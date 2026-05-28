import pygame
import queue
import threading
from typing import Optional
from collections import defaultdict

from src.ui.loaders import element_detector
from src.ui.elements import Button, TextInput, LoadingIcon

from src.functions.functions_registry import (internal_functions_registry, 
                                              external_functions_registry)


def screens_loader(display_cfg: dict, screens_cfg: dict) -> dict:
    '''
    Initializes all application screens from configuration data.

    Args:
        display_cfg (dict): Global display and asset settings.
        screens_cfg (dict): Layout and element definitions for each screen.

    Returns:
        dict: A dictionary of initialized screen objects indexed by name.
    '''
    screens = dict()
    for screen_cfg in screens_cfg.values():
        screens[screen_cfg['ID']] = Screen(display_cfg=display_cfg,
                                           screen_cfg=screen_cfg)
    return screens


class Screen:
    '''
    Represents a single app state or menu, managing its own UI elements.

    Attributes:
        display_cfg (dict): Global display and asset settings.
        screen_cfg (dict): Specific configuration for this screen instance.
        elements_cfg (dict): Raw dict containing the config of UI elements.
        colors (dict): Reference to the global color palette.
        fonts (dict): Reference to the pre-loaded font objects.
        elements (list): List of instantiated UI component objects: Buttons...
        buttons (list): A filtered list containing only the Button objects for 
                        event handling.
        external_registry (dict): Mapping of string identifiers to 
                                  Python functions.
    '''

    def __init__(self, display_cfg: dict, screen_cfg: dict):
        '''
        Initializes the screen and its components from configuration.
        '''
        self.internal_registry = internal_functions_registry
        self.external_registry = external_functions_registry
        funcs_registry = self.internal_registry | self.external_registry
        self.func_from_registry_is_running = False

        self.display_cfg = display_cfg
        self.screen_cfg = screen_cfg
        self.elements_cfg = screen_cfg['elements']

        self.colors = display_cfg['colors']
        self.fonts = display_cfg['fonts']

        self.elements = element_detector(display_cfg=self.display_cfg,
                                         elements_cfg=self.elements_cfg,
                                         funcs_registry = funcs_registry)

        # Controls: Elements that user can interact with
        ctrl_types = {Button, TextInput}
        self.controls = [el for el in self.elements if type(el) in ctrl_types]

        self.functions_hooks = defaultdict(list)
        hook_types = {LoadingIcon}
        for el in self.elements:
            if type(el) in hook_types:
                self.functions_hooks[el.func].append(el)

        # Tasks manager
        self.task_queue = queue.Queue()

        self.worker = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker.start()


    def draw(self, screen) -> None:
        '''
        Renders the background and all UI elements to the surface.

        Args:
            screen (pygame.Surface): The main display surface where elements 
                                     will be drawn.
        '''
        screen.fill(self.colors['background'])        
        for el in self.elements:
            el.draw(screen)


    def handle_events(self, event: pygame.event.Event) -> Optional[str]:
        '''
        Processes user input and interactions for this specific screen.

        Args:
            event (pygame.event.Event): The current event from the pygame 
                                        event queue.
        '''
        if event.type == pygame.QUIT:
            return 'exit'
        
        for element in self.controls:
            response = element.handle_events(event)
            
            if response:
                return self._process_element_response(response)
                    
        return None
    

    def _process_element_response(self, response: dict) -> Optional[str]:
        '''
        Centralizes the logic for executing functions and handling redirections.
        
        Args:
            response (dict): Data returned by an interactive element's handle_events.
            
        Returns:
            str | None: The redirection target if present, else None.
        '''
        functions = response.get('functions', [])

        for func_name in functions:
            if not func_name: continue
            
            if func_name == 'exit':
                return 'exit'
            
            # --- MULTITHREADING LOGIC ---
            internal_check = self.internal_registry.get(func_name)
            external_check = self.external_registry.get(func_name)
            func = internal_check or external_check
        
            if callable(func):
                hooks = self._get_hooks_for_func(func_name)

                self.task_queue.put((func, hooks, func_name))

                print('--- TASK ADDED ---')
                print(f'TASKS QUEUE: {self.task_queue}')

            else:
                print(f'ERROR: Function "{func_name}" not found.')

        return response.get('redirection')
    

    def _get_hooks_for_func(self, func_name):
        '''
        
        '''
        return self.functions_hooks.get(func_name, [])


    def _worker_loop(self):
        '''
        This loop runs perpetually in the background thread.
        '''
        while True:

            func, hooks, func_name = self.task_queue.get()
            
            print(f'--- STARTING: {func_name} ---')
            for hook in hooks:
                hook.is_running = True    
            
            try:
                func(self)

            finally:
                for hook in hooks:
                    hook.is_running = False
                
                self.task_queue.task_done()

                print('--- TASK DONE ---')
                print(f'TASKS QUEUE: {self.task_queue}')


if __name__ == '__main__':
    pass    