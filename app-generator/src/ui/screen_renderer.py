import pygame

from src.ui.loaders import title_loader, buttons_loader 
import src.ui.app_functions


app_functions_registry = {
    "reset": src.ui.app_functions.reset_maze,
    "save": src.ui.app_functions.save_data,
}

def screens_loader(window: dict, colors: dict, fonts: dict, config: dict) -> dict:

    screens = dict()
    for screen_cfg in config.values():
        screens[screen_cfg['name']] = Screen(window=window, colors=colors, 
                                            fonts=fonts, config=screen_cfg)
    return screens


class Screen:

    # TO-DO: Aqui llamar a la funcion "element_detector()" en loaders.py

    def __init__(self, window: dict, colors: dict, fonts: dict, config: dict):
        self.window = window
        self.colors = colors
        self.fonts = fonts
        
        self.width = window['width']
        self.height = window['height']

        self.return_button = config['return_button']
        self.title = title_loader(config=config['title'], colors=colors, 
                                      fonts=fonts, window=self.window)
        self.buttons = buttons_loader(config=config['buttons'], colors=colors, 
                                      fonts=fonts)
        
        self._external_registry = app_functions_registry

    def draw(self, screen):
        '''All the rendering logic is encapsulated here'''
        screen.fill(self.colors['background'])
        
        # Draw title
        self.title.drawing(screen)

        if self.return_button['has_return']:
            if self.return_button['redirection'] == 'None':
                #TO-DO: draw return button and config redirection.
                # Un goto hacia el que diga el cofig.
                pass
        
        # Draw buttons
        for button in self.buttons:
            button.drawing(screen)


    def handle_events(self, event):
        '''Manage events logic on the screen'''
        if event.type == pygame.QUIT:
            return "exit"
        
        for button in self.buttons:
            if button.button_clicked(event):
                actions = button.get_actions()
                
                # Priority 1: Internal function/s
                if "function" in actions["type"]:
                    for func_name in actions["call"]:
                        if func_name == "exit":
                            return "exit"
                        self._execute_internal_function(func_name)
                
                # Priority 2: redirection (GOTO)
                if "goto" in actions["type"]:
                    return actions["goto"]
                    
        return None
    
    
    def _execute_internal_function(self, func_name):
        """
        Retrieves a function from the registry and executes it.
        
        Uses Dependency Injection by passing 'self' (current screen instance) 
        as an argument, allowing the external function to access and modify 
        the screen's state or data.
        """
        func = self._external_registry.get(func_name)
        
        if func:
            func(self) 
        else:
            print(f"ERROR: Function '{func_name}' is not registered.")


if __name__ == "__main__":
    pass