import pygame
from pathlib import Path

from src.ui.elements import Button, Text


def element_detector(display_cfg: dict, elements_cfg: dict) -> list:

    categories = {'button': [], 'image': [], 'text': []}

    for el in elements_cfg:
        categories[elements_cfg[el]['type']].append(elements_cfg[el])

    buttons_cfg = categories['button']
    images_cfg = categories['image']
    texts_cfg = categories['text']

    output = []

    if buttons_cfg:
        buttons = buttons_loader(display_cfg=display_cfg,
                                     buttons_cfg=buttons_cfg)
        output += buttons
        
    if images_cfg:
        images = []
        output += images
    
    if texts_cfg:
        texts = texts_loader(display_cfg=display_cfg, texts_cfg=texts_cfg)
        output += texts
    
    return output
    
    
def buttons_loader(display_cfg: dict, buttons_cfg: dict) -> list:
    '''
    Parses button configuration data to instantiate UI Button objects.

    Args:
        config (dict): Nested dictionary containing button configuration.
        colors (dict): Global RGB color palette mapping.
        fonts (dict): Pre-loaded pygame.font.Font objects.

    Returns:
        list: A collection of initialized Button instances.
    '''
    buttons = []
    for button_cfg in buttons_cfg:
        buttons.append(Button(display_cfg=display_cfg, button_cfg=button_cfg))
    return buttons


def texts_loader(display_cfg: dict, texts_cfg: dict) -> list:
    '''
    Parses text configuration data to instantiate UI Text objects.

    Args:
        config (dict): Nested dictionary containing button configuration.
        colors (dict): Global RGB color palette mapping.
        fonts (dict): Pre-loaded pygame.font.Font objects.

    Returns:
        list: A collection of initialized Button instances.
    '''
    texts = []
    for text_cfg in texts_cfg:
        texts.append(Text(display_cfg=display_cfg, text_cfg=text_cfg))
    return texts


def fonts_loader(fonts_cfg: dict) -> dict:
    '''
    Resolves filesystem paths and initializes Pygame font assets.

    Uses pathlib for robust cross-platform path resolution, moving from the 
    current script location to the project root's asset directory.

    Args:
        config (dict): Mapping of font keys to file names and point sizes.

    Returns:
        dict: A dictionary where keys match config and values are 
        pygame.font.Font objects.
    '''

    # Locate root (from maze-solver-app/src/utils/ to maze-solver-app/)
    root_path = Path(__file__).resolve().parent.parent.parent
    fonts_path = root_path / 'assets' / 'fonts' 

    fonts = {}
    for key, data in fonts_cfg.items():
        path = fonts_path / data['file']
        # Convert Path object to string for Pygame compatibility
        fonts[key] = pygame.font.Font(str(path), data['size'])

    return fonts


if __name__ == '__main__':
    pass