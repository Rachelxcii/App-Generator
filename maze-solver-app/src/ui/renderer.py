import pygame 
from src.ui.elements import Button
from src.utils.config_loader import get_config

from src.ui.fonts_loader import (font_sml_button, font_mid_button, 
                                 font_big_button, font_main_title)

def main_screen():
    """
    Renders the main menu of the Maze Generator & Solver.
    
    Args:
        config (dict): Global configuration loaded from JSON.
        fonts (dict): Pre-loaded pygame.font.Font objects.
    """

    # 1. Initialize Window Settings from Config
    pygame.init()
    width, height = 700, 500
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Maze Generator & Solver")
    
    font_title = font_main_title
    clock = pygame.time.Clock()

    # 2. UI Layout Constants
    # Using layout logic based on screen dimensions for responsiveness
    buttons = []


    # 2.1 Main buttons: "Generator", "Solver", "Dashboard"
    buttons_name = ["Generator", "Solver", "Dashboard"]
    
    width_b, height_b, space_b, left_space = 150, 150, 75, 50
    y_pos = 250 # + ((400 - 250) // 2)
    
    for i, nombre in enumerate(buttons_name):
        # Horizontal space between buttons: space_b
        x_pos = left_space + (i * width_b) + (i * space_b)
        buttons.append(Button(x_pos, y_pos, width_b, height_b, nombre, 
                              font_sml_button, (50, 50, 50), (100, 100, 100)))
    

    # 2.1 Auxiliar buttons: "Reset", "Exit"
    buttons_name = ["Reset", "Exit"]
    
    width_b, height_b, space_b, left_space = 100, 50, 200, 150
    y_pos = 450 - height_b//2
    
    for i, nombre in enumerate(buttons_name):
        # Horizontal space between buttons: space_b
        x_pos = left_space + (i * width_b) + (i * space_b)
        buttons.append(Button(x_pos, y_pos, width_b, height_b, nombre, 
                              font_sml_button, (50, 50, 50), (100, 100, 100)))

    is_running = True
    while is_running:
        screen.fill((30, 30, 30)) # Dark background
        
        # 1. Title drawing block
        txt_title = font_title.render("MAZE SOLVER", True, (200, 200, 200))
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
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main_screen()