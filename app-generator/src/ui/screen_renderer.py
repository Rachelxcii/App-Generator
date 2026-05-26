import pygame
from typing import Optional

import src.ui.external_functions
import src.ui.internal_functions
from src.ui.loaders import element_detector
from src.ui.elements import Button, TextInput


internal_functions_registry = {
    'reset': src.ui.internal_functions.reset_maze,
    'save': src.ui.internal_functions.save_data,
}

external_functions_registry = {
    
}


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
        self.display_cfg = display_cfg
        self.screen_cfg = screen_cfg
        self.elements_cfg = screen_cfg['elements']

        self.colors = display_cfg['colors']
        self.fonts = display_cfg['fonts']

        self.elements = element_detector(display_cfg=self.display_cfg,
                                         elements_cfg=self.elements_cfg)
        
        self.buttons = [el for el in self.elements if type(el) == Button]
        self.text_inputs = [el for el in self.elements if type(el) == TextInput]

        ctrl_types = {Button, TextInput}

        self.controls = [el for el in self.elements if type(el) in ctrl_types]

        self.internal_registry = internal_functions_registry
        self.external_registry = external_functions_registry


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
            
            if not self._execute_internal_function(func_name):
                self._execute_external_function(func_name)

        return response.get('redirection')
    

    def _execute_internal_function(self, func_name):
        '''
        Retrieves a function from the internal registry, executes it and 
        returns True, if the function exists.
        If the function doesn't exist, return False.
        '''
        func = self.internal_registry.get(func_name)
        if callable(func):
            func(self)
            return True
        return False


    def _execute_external_function(self, func_name):
        '''
        Retrieves a function from the external registry, executes it, 
        if the function exists.
        If the function doesn't exist, prints ERROR.
        '''
        func = self.external_registry.get(func_name)
        if callable(func):
            func(self)
        else:
            print(f'ERROR: Function "{func_name}" not found in any registry.')


if __name__ == '__main__':
    pass