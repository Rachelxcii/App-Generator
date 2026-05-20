import pygame

import src.ui.app_functions
from src.ui.loaders import element_detector
from src.ui.elements import Button


app_functions_registry = {
    "reset": src.ui.app_functions.reset_maze,
    "save": src.ui.app_functions.save_data,
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
        '''
        screen.fill(self.colors['background'])        
        for el in self.elements:
            el.draw(screen)


    def handle_events(self, event) -> None:
        '''
        Processes user input and interactions for this specific screen.
        '''
        if event.type == pygame.QUIT:
            return "exit"
        
        for button in self.buttons:
            if button.button_clicked(event):
                actions = button.get_actions()
                
                # Priority 1: Internal functions
                #if "functions" in actions["type"]:
                if actions["functions"]:
                    for func_name in actions["functions"]:
                        if func_name == "exit":
                            return "exit"
                        self._execute_internal_function(func_name)
                
                # Priority 2: redirection
                #if "redirection" in actions["type"]:
                if actions["redirection"]:
                    return actions["redirection"]
                    
        return None
    
    
    def _execute_internal_function(self, func_name):
        """
        Retrieves a function from the registry and executes it.
        
        Uses Dependency Injection by passing 'self' (current screen instance) 
        as an argument, allowing the external function to access and modify 
        the screen's state or data.
        """
        func = self.external_registry.get(func_name)
        
        if func:
            func(self) 
        else:
            print(f"ERROR: Function '{func_name}' is not registered.")


if __name__ == "__main__":
    pass