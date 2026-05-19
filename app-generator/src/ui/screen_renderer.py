import pygame

import src.ui.app_functions
from src.ui.loaders import element_detector
from src.ui.elements import Button


app_functions_registry = {
    "reset": src.ui.app_functions.reset_maze,
    "save": src.ui.app_functions.save_data,
}

def screens_loader(display_cfg: dict, screens_cfg: dict) -> dict:
    '''Create every screen from the screens configuration'''
    screens = dict()
    for screen_cfg in screens_cfg.values():
        screens[screen_cfg['ID']] = Screen(display_cfg=display_cfg,
                                           screen_cfg=screen_cfg)
    return screens


class Screen:

    def __init__(self, display_cfg: dict, screen_cfg: dict):
        
        self.display_cfg = display_cfg
        self.screen_cfg = screen_cfg
        self.elements_cfg = screen_cfg['elements']

        self.colors = display_cfg['colors']
        self.fonts = display_cfg['fonts']

        self.elements = element_detector(display_cfg=self.display_cfg,
                                         elements_cfg=self.elements_cfg)
        
        print(f'ELEMENTS SCREEN: {self.elements}')

        self.buttons = [el for el in self.elements if type(el) == Button]
        
        for el in self.elements:
            print(f'--- ELEMENT NAME: {el}')
            print(f'--- ELEMENT TYPE: {type(el)}')

        print(f'BUTTONS SCREEN: {self.buttons}')
                
        self.external_registry = app_functions_registry


    def draw(self, screen) -> None:
        '''Draw every element of the current screen'''
        screen.fill(self.colors['background'])        
        for el in self.elements:
            el.draw(screen)


    def handle_events(self, event) -> None:
        '''Manage events logic on the screen'''
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