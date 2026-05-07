import pygame

from src.utils.config_loader import get_config
from src.ui.font_loader import load_all_fonts
#from src.ui.renderer import main_screen


# Load configuration
config = get_config()

# Initialize pygame font
if not pygame.font.get_init():
    pygame.font.init()

# Load fonts
fonts = load_all_fonts(config_fonts=config['fonts'])


if __name__ == '__main__':
    print(f'CONFIG: {config}')
    #main_screen(config_screen=config['main_screen'])