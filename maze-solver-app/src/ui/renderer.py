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











    
def main_screen(
        window: dict, colors: dict, fonts: dict, config_screen: dict
        ) -> None:
    """
    Renders the main menu of the Maze Generator & Solver.
    
    Args:
        config (dict): Global configuration loaded from JSON.
        fonts (dict): Pre-loaded pygame.font.Font objects.
    """

    # 1. Initialize Window Settings from Config
    pygame.init()
    width, height = window['width'], window['height']
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Maze Generator & Solver")
    
    font_title = fonts['main_title']
    clock = pygame.time.Clock()


    # 2 Load main screen buttons    
    # Using layout logic based on screen dimensions for responsiveness
    
    buttons = buttons_loader(config=config_screen['buttons'], 
                             colors=colors, fonts=fonts)

    is_running = True
    while is_running:
        screen.fill(colors['background']) # Dark background
        
        # 1. Title drawing block
        txt_title = font_title.render("MAZE SOLVER", True, colors['title_txt'])
        screen.blit(txt_title, (width // 2 - txt_title.get_width() // 2, 50))

        # 2. Event handling block
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            
            # Detect button clicked
            for button in buttons:
                if button.button_clicked(event):
                    print(f"Has pulsado: {button.text}")
                    if button.text == "Salir":
                        is_running = False

        # 3. Buttons drawing block
        for button in buttons:
            button.drawing(screen)

        pygame.display.flip()
        clock.tick(window['fps'])

    pygame.quit()

if __name__ == "__main__":
    main_screen()