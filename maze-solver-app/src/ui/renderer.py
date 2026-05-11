import pygame

from src.ui.loaders import buttons_loader


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
    
    buttons = buttons_loader(config=config_screen, colors=colors, fonts=fonts)

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