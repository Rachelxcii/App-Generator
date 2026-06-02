import pygame
import queue
import threading
import sys

from src.utils.config_loader import get_config
from src.ui.loaders import fonts_loader
from src.ui.screen_renderer import screens_loader
from src.utils.path_loader import AppPaths


# --- TO-DO LIST ---
# TO-DO: pre-sets functions like: save CSV, reset, exit, etc. (internal_functions.py)
# TO-DO: tests to check the entire config JSON
# TO-DO: 

class App:

    def __init__(self):
        # --- Global Initialization and Asset Mapping ---
        # Load global application settings from JSON
        self.config = get_config()

        # Load path registry for internal reference
        self.paths = AppPaths().to_dict()

        # Ensure the Pygame font module is ready for asset loading
        if not pygame.font.get_init():
            pygame.font.init()

        # Load ui configuration
        self.display_cfg = self.config['display']
        self.display_cfg['paths'] = self.paths
        self.display_cfg['fonts'] = fonts_loader(display_cfg=self.config['display'])

        self.screens_cfg = {k: v for k, v in self.config.items() if k.endswith("_screen")}

        # Tasks manager (for Thread-Safe)
        self.task_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.running = True
        self.closing_mode = False
        self.await_all_tasks = self.display_cfg['await_all_tasks']
        
        # Only one worker thread
        self.worker_thread = threading.Thread(target=self._worker_loop, 
                                              daemon=True)
        self.worker_thread.start()

        # Initialize base display
        pygame.init()
        self.display = pygame.display.set_mode((self.display_cfg['width'], 
                                                self.display_cfg['height']))
        pygame.display.set_caption("My App Framework")

        # Dictionary containing instantiated screen objects mapped by their ID
        self.screens = screens_loader(display_cfg=self.display_cfg, 
                                      screens_cfg=self.screens_cfg,
                                      shared_tasks=self.task_queue)
        
        # Set the starting point for the state machine
        self.current_state = self.display_cfg['init_screen']

        # Frame rate controller
        self.clock = pygame.time.Clock()


    def _worker_loop(self):
        '''
        This loop runs perpetually in the background thread.
        '''
        while self.running:
            try:
                task = self.task_queue.get(timeout=0.5)

                if task == "SHUTDOWN":
                    self.task_queue.task_done()
                    break
                
                # Saving all parameter of the task
                screen_id = task['screen_id']
                func_name = task['func_name']
                func = task['func']
                inputs = task['inputs']
                hooks = task['hooks']
                
                for hook in hooks:
                    hook.is_running = True
                
                try:
                    result = func(screen_id, inputs)
                    response = {
                        'screen_id': screen_id,
                        'func_name': func_name,
                        'result': result
                    }
                    print(f'MAIN RESPONSE: {response}')

                    self.result_queue.put(response)

                finally:
                    for hook in hooks:
                        hook.is_running = False
                    
                    self.task_queue.task_done()

            except queue.Empty:
                continue
            except Exception as e:
                print(f"--- WORKER ERROR CRÍTICO: {e} ---")


    def check_worker_results(self):
        '''
        
        '''
        try:
            while not self.result_queue.empty():
                response = self.result_queue.get_nowait()
                
                screen_id = response['screen_id']
                func_name = response['func_name']
                result = response['result']
                
                if screen_id in self.screens:
                    self.screens[screen_id].resolve_output(func_name=func_name,
                                                           result=result)
                self.result_queue.task_done()
        except queue.Empty:
            pass


    def run(self):
        '''
        Main execution loop. Initializes the display and manages state transitions 
        between different application screens.

        Logic:
            1. Initializes the Pygame display surface and clock.
            2. Loads all screen objects based on the configuration.
            3. Enters the main loop: 
            - Handles events through the active screen.
            - Updates current_state if a transition (redirection) is triggered.
            - Renders the active screen at the defined FPS.
        '''

        # --- MAIN APPLICATION LOOP ---
        while True: # self.current_state != 'exit' or self.closing_mode:
            
            # Checks definitive exit
            if self.closing_mode and not self.worker_thread.is_alive():
                print("--- APP: THREAD FINISHED, CLOSING PROCESS ---")
                break

            active_screen = self.screens[self.current_state] # Dict: screen_name: Screen()
            self.check_worker_results()

            # Events manager
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self._initiate_shutdown()

                if not self.closing_mode:  # TO-DO: Solo procesamos eventos si no estamos cerrando
                    new_state = active_screen.handle_events(event)
                    if new_state == 'exit':
                        self._initiate_shutdown()
                    elif new_state == 'cancel_pending_tasks':
                        self._cancel_pending_tasks()
                    elif new_state:
                        self.current_state = new_state

            # Render
            active_screen.draw(self.display)
            pygame.display.flip()
            self.clock.tick(self.display_cfg['fps'])

        pygame.quit()
        sys.exit()


    def _initiate_shutdown(self):
        '''
        Prepares app for a controlled shutdown TO-DO: revision gramatica
        '''
        if not self.closing_mode:
            print("--- INITIATING CONTROLLED SHUTDOWN ---")
            self.closing_mode = True
            
            # Informar a la pantalla actual para que dibuje el "CLOSING THE APP"
            self.screens[self.current_state].is_closing = True
            
            # Limpiar cola y enviar señal de parada
            if not self.await_all_tasks:
                self._cancel_pending_tasks()
            
            self.task_queue.put("SHUTDOWN")

    
    def _cancel_pending_tasks(self):
        try:
            while not self.task_queue.empty():
                self.task_queue.get_nowait()
                self.task_queue.task_done()
        except queue.Empty:
            pass


if __name__ == '__main__':
    app = App()
    app.run()