import pygame

import src.ui.external_functions
import src.ui.internal_functions
from src.ui.loaders import element_detector
from src.ui.elements import Button


app_functions_registry = {
    "reset": src.ui.internal_functions.reset_maze,
    "save": src.ui.internal_functions.save_data,
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
        self.external_registry = app_functions_registry


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


    def handle_events(self, event) -> None:
        '''
        Processes user input and interactions for this specific screen.

        Args:
            event (pygame.event.Event): The current event from the pygame 
                                        event queue.
        '''
        if event.type == pygame.QUIT:
            return "exit"
        
        for button in self.buttons:
            if button.button_clicked(event):
                actions = button.get_actions()
                
                if actions["functions"]:
                    for func_name in actions["functions"]:
                        if func_name == "exit":
                            return "exit"
                        self._execute_external_function(func_name)
                
                if actions["redirection"]:
                    return actions["redirection"]
                    
        return None
    
    
    def _execute_external_function(self, func_name):
        """
        Retrieves a function from the registry and executes it.
        
        Uses Dependency Injection by passing 'self' (current screen instance) 
        as an argument, allowing the external function to access and modify 
        the screen's state or data.

        Args:
            func_name (str): The unique identifier of the function within 
                             the external registry.
        """
        func = self.external_registry.get(func_name)
        
        if func:
            func(self) 
        else:
            print(f"ERROR: Function '{func_name}' is not registered.")


if __name__ == "__main__":
    pass