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
        print(f"[INFO] Initializing Application Framework...")

        # --- Asset & Config Loading ---
        try:
            self.config = get_config()
            self.paths = AppPaths().to_dict()
            print(f"[INFO] Configuration and Paths loaded successfully.")
        except Exception as e:
            print(f"[ERROR] Failed to load configuration: {e}")
            sys.exit(1)

        if not pygame.font.get_init():
            pygame.font.init()

        # Load ui configuration
        self.display_cfg = self.config['display']
        self.display_cfg['paths'] = self.paths

        print(f"[INFO] Loading system fonts...")
        self.display_cfg['fonts'] = fonts_loader(display_cfg=self.config['display'])

        self.screens_cfg = {k: v for k, v in self.config.items() if k.endswith("_screen")}

        # Tasks manager (for Thread-Safe)
        self.task_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.running = True
        self.closing_mode = False
        self.await_all_tasks = self.display_cfg['await_all_tasks']
        
        # Threading (Only one worker thread)
        print(f"[INFO] Starting Worker Thread...")
        self.worker_thread = threading.Thread(target=self._worker_loop, 
                                              daemon=True)
        self.worker_thread.start()

        # Pygame setup
        pygame.init()
        self.display = pygame.display.set_mode((self.display_cfg['width'], 
                                                self.display_cfg['height']))
        pygame.display.set_caption("My App Framework")

        # Screen Instantiation
        # Dictionary containing instantiated screen objects mapped by their ID
        print(f"[INFO] Instantiating {len(self.screens_cfg)} screens...")
        self.screens = screens_loader(display_cfg=self.display_cfg, 
                                      screens_cfg=self.screens_cfg,
                                      shared_tasks=self.task_queue)
        
        # Set the starting point for the state machine
        self.current_state = self.display_cfg['init_screen']
        print(f"[INFO] Entry point set to screen: '{self.current_state}'")

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
                    print("[INFO] Worker Thread: Shutdown signal received.")
                    self.task_queue.task_done()
                    break
                
                screen_id = task['screen_id']
                func_name = task['func_name']
                func = task['func']
                inputs = task['inputs']
                hooks = task['hooks']

                print(f"[INFO] Worker: Executing '{func_name}' for screen '{screen_id}'")
                
                for hook in hooks:
                    hook.is_running = True
                
                try:
                    result = func(screen_id, inputs)
                    response = {
                        'screen_id': screen_id,
                        'func_name': func_name,
                        'result': result
                    }
                    self.result_queue.put(response)
                    print(f"[INFO] Worker: Task '{func_name}' finished successfully.")

                finally:
                    for hook in hooks:
                        hook.is_running = False
                    self.task_queue.task_done()

            except queue.Empty:
                continue

            except Exception as e:
                print(f"[ERROR] Worker: Critical internal loop error: {e}")


    def check_worker_results(self):
        '''
        
        '''
        try:
            while not self.result_queue.empty():
                response = self.result_queue.get_nowait()
                
                screen_id = response['screen_id']
                func_name = response['func_name']
                
                if screen_id in self.screens:
                    print(f"[INFO] Main: Dispatching result of '{func_name}' to screen '{screen_id}'")
                    self.screens[screen_id].resolve_output(func_name=func_name, result=response['result'])
                else:
                    print(f"[WARNING] Main: Received result for inactive/missing screen '{screen_id}'")
                
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

        print("[INFO] Entering Main Application Loop.")
        while True:
            
            if self.closing_mode and not self.worker_thread.is_alive():
                print("[INFO] App: All threads finished. Finalizing shutdown.")
                break

            active_screen = self.screens[self.current_state] # Dict: screen_name: Screen()
            self.check_worker_results()

            
            for event in pygame.event.get(): # Events manager

                if event.type == pygame.QUIT:
                    self._initiate_shutdown()

                if not self.closing_mode:
                    new_state = active_screen.handle_events(event)
                    if new_state == 'exit':
                        self._initiate_shutdown()
                    elif new_state == 'cancel_pending_tasks':
                        self._cancel_pending_tasks()
                    elif new_state:
                        print(f"[INFO] Screen Transition: '{self.current_state}' -> '{new_state}'")
                        self.current_state = new_state

            # Renders
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
            print("[WARNING] Shutdown initiated. Waiting for worker thread...")
            self.closing_mode = True
            
            # Informar a la pantalla actual para que dibuje el "CLOSING THE APP"
            self.screens[self.current_state].is_closing = True
            
            # Limpiar cola y enviar señal de parada
            if not self.await_all_tasks:
                self._cancel_pending_tasks()
            
            self.task_queue.put("SHUTDOWN")

    
    def _cancel_pending_tasks(self):
        '''
        
        '''
        count = 0
        try:
            while not self.task_queue.empty():
                self.task_queue.get_nowait()
                self.task_queue.task_done()
                count += 1
            if count > 0:
                print(f"[WARNING] Cancelled {count} pending tasks in queue.")

        except queue.Empty:
            pass


if __name__ == '__main__':
    app = App()
    app.run()