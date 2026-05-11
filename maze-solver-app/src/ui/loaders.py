from pathlib import Path
import pygame

def fonts_loader(config_fonts: dict) -> dict:
    '''
    
    '''
    # Locate root (from maze-solver-app/src/utils/ to maze-solver-app/)
    root_path = Path(__file__).resolve().parent.parent.parent
    fonts_path = root_path / 'assets' / 'fonts' 

    fonts = {}
    for key, data in config_fonts.items():
        path = fonts_path / data['file']
        fonts[key] = pygame.font.Font(str(path), data['size'])

    return fonts

def buttons_loader():
    pass


if __name__ == '__main__':
    pass