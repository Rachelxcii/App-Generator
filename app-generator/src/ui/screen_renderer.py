import pygame
import queue
from typing import Optional
from collections import defaultdict

from src.ui.loaders import element_detector

from src.ui.elements.button import Button
from src.ui.elements.loading_icon import LoadingIcon
from src.ui.elements.text_input import TextInput

from src.functions.functions_registry import (internal_functions_registry, 
                                              external_functions_registry)


def screens_loader(
        display_cfg: dict, screens_cfg: dict, shared_tasks: queue
        ) -> dict:
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
        screens[screen_cfg['ID']] = Screen(screen_id=screen_cfg['ID'],
                                           display_cfg=display_cfg,
                                           screen_cfg=screen_cfg,
                                           shared_tasks=shared_tasks)
    return screens


class Screen:
    '''
    Manages a specific application state, UI lifecycle, and event delegation.

    The Screen class orchestrates the interaction between data-driven UI 
    elements and logic execution. It acts as a bridge between user input, 
    the function registry, and the Worker Thread's task queue.

    Attributes:
        screen_id (str): Unique identifier for the current state/menu.
        display_cfg (dict): Global display and asset settings.
        screen_cfg (dict): Configuration schema for this specific screen.
        elements (list): All UI components (visual and interactive).
        controls (list): Subset of elements that capture user input.
        functions_hooks (defaultdict): Mapping of function names to UI elements 
                                       that react to their execution status.
        shared_tasks (queue.Queue): Thread-safe queue for dispatching tasks 
                                    to the Worker.
    '''

    def __init__(self, screen_id: str, display_cfg: dict, screen_cfg: dict, 
                 shared_tasks: queue):
        '''
        Initializes the screen environment and instantiates its UI component 
        tree.

        Args:
            screen_id (str): Name of the screen.
            display_cfg (dict): Global configuration for styles and resources.
            screen_cfg (dict): JSON-derived dictionary for screen elements.
            shared_tasks (queue.Queue): Communication channel for the Worker Thread.
        '''
        self.internal_registry = internal_functions_registry
        self.external_registry = external_functions_registry
        funcs_registry = self.internal_registry | self.external_registry
        print(type(funcs_registry))
        self.func_from_registry_is_running = False

        self.screen_id = screen_id
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

        # Hooks
        self.functions_hooks = defaultdict(list)
        hook_types = {LoadingIcon}
        for el in self.elements:
            if type(el) in hook_types:
                self.functions_hooks[el.func].append(el)

        # Shared tasks queue
        self.shared_tasks = shared_tasks


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
        Delegates Pygame events to interactive controls and processes 
        responses.

        Args:
            event (pygame.event.Event): Current event from the main loop.

        Returns:
            Optional[str]: Redirection target or command (e.g., 'exit') 
                           if triggered.
        '''
        if event.type == pygame.QUIT:
            return 'exit'

        for element in self.controls:
            response = element.handle_events(event)
            
            if response:
                print(f'RESPONSE: {response}')
                return self._process_element_response(response)
                    
        return None
    

    def _process_element_response(self, response: dict) -> Optional[str]:
        '''
        Translates UI responses into executable actions or Worker Thread tasks.

        Args:
            response (dict): Data payload from an element
                             (functions, inputs, redirections).
            
        Returns:
            Optional[str]: Redirection screen ID if requested by the element.
        '''
        functions = response.get('functions', [])

        for func_name in functions:
            if not func_name: continue
            
            if func_name == 'exit':
                return 'exit'
            
            if func_name == 'cancel_pending_tasks':
                return 'cancel_pending_tasks'
            
            internal_check = self.internal_registry.get(func_name)
            external_check = self.external_registry.get(func_name)
            func = internal_check or external_check
        
            if callable(func):
                # Adding function, its inputs and hooks to the worker thread
                inputs = self._collect_inputs(response.get('inputs', []))
                hooks = self._get_hooks_for_func(func_name)
                #self.shared_tasks.put((self.screen_id, func_name, func, hooks))
                new_task = {'screen_id': self.screen_id, 
                            'func_name': func_name, 
                            'func': func, 
                            'inputs': inputs,
                            'hooks': hooks}
                self.shared_tasks.put(new_task)

            else:
                print(f'ERROR: Function "{func_name}" not found.')

        return response.get('redirection')
    

    def _collect_inputs(self, input_ids: list) -> dict:
        '''
        Gathers current values from specified UI input elements.

        Args:
            input_ids (list): IDs of the TextInputs to scrape data from.

        Returns:
            dict: Mapping of element IDs to their current text content.
        '''
        collected_values = {}
        for element in self.controls:
            if getattr(element, 'id', None) in input_ids:
                if element.text != element.placeholder:
                    collected_values[element.id] = element.text
        return collected_values
    

    def _get_hooks_for_func(self, func_name):
        '''
        Retrieves UI elements that need to react when a specific function runs.
        '''
        return self.functions_hooks.get(func_name, [])
