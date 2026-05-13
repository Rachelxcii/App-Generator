import pygame

from src.ui.loaders import title_loader, buttons_loader 

import pygame


class Screen:
    # TO-DO clase base que contenga: draw, handle events.
    pass


class MainScreen:

    def __init__(self, window: dict, colors: dict, fonts: dict, config: dict):
        self.window = window
        self.colors = colors
        self.fonts = fonts
        
        self.width = window['width']
        self.height = window['height']

        self.has_return = config['has_return']
        self.title = title_loader(config=config['title'], colors=colors, 
                                      fonts=fonts, window=self.window)
        self.buttons = buttons_loader(config=config['buttons'], colors=colors, 
                                      fonts=fonts)

    def draw(self, screen): #TO-DO este metodo a Screen class
        '''All the rendering logic is encapsulated here'''
        screen.fill(self.colors['background'])
        
        # Draw title
        # TO-DO Lógica encapsulada: _draw_title(screen), create Title class?
        self.title.drawing(screen)

        if self.has_return:
            #TO-DO print return button
            pass
        
        # Draw buttons
        # TO-DO Lógica encapsulada: drawing method for Button class DONE
        for button in self.buttons:
            button.drawing(screen)

    def handle_events(self, event):
        '''Manage events logic on the screen'''
        if event.type == pygame.QUIT:
            return "exit"
        
        for button in self.buttons:
            if button.button_clicked(event):
                # Devolvemos la acción para que el orquestador decida
                return 'MAIN-SCREEN' # TO-DO cambiar este valor por el de goto
                # return button.text.lower() -> esto devuelve el nombre del 
                # boton pulsado, deberia devolver la action goto la screen que sea.
        return None


class DashboardScreen:
    pass


class SolverScreen:
    pass


if __name__ == "__main__":
    main_screen()