import pygame

from src.utils.config_loader import get_config
from src.ui.loaders import fonts_loader
from src.ui.renderer import main_screen


# Load configuration
config = get_config()

# Initialize pygame font
if not pygame.font.get_init():
    pygame.font.init()

# Load ui configuration
window = config['window']
colors = config['colors']
fonts = fonts_loader(config_fonts=config['fonts'])


if __name__ == '__main__':
    main_screen(
        window=window,  
        colors=colors,
        fonts=fonts,
        config_screen=config['main_screen']
        )