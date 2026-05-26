import pygame
from collections import defaultdict

from src.ui.elements import Button, Image, Text


def element_detector(display_cfg: dict, elements_cfg: dict) -> list:
    '''
    Identifies and instantiates UI objects from elements configuration.

    Args:
        display_cfg (dict): Global display and asset settings.
        elements_cfg (dict): Raw dict containing the config of UI elements.

    Returns:
        list: A list of initialized UI component objects (Buttons, Texts ...).
    '''
    categories = defaultdict(list)

    for id, el_cfg in elements_cfg.items():
        el_cfg['id'] = id
        categories[el_cfg.get('type', 'unknown')].append(el_cfg)

    buttons_cfg = categories['button']
    images_cfg = categories['image']
    texts_cfg = categories['text']

    output = []

    if buttons_cfg:
        buttons = buttons_loader(display_cfg=display_cfg,
                                     buttons_cfg=buttons_cfg)
        output += buttons
        
    if images_cfg:
        images = images_loader(display_cfg=display_cfg, images_cfg=images_cfg)
        output += images
    
    if texts_cfg:
        texts = texts_loader(display_cfg=display_cfg, texts_cfg=texts_cfg)
        output += texts
    
    return output
    
    
def buttons_loader(display_cfg: dict, buttons_cfg: dict) -> list:
    '''
    Parses button configuration data to instantiate UI Button objects.

    Args:
        display_cfg (dict): Global display and asset settings.
        buttons_cfg (dict): Nested dictionary containing buttons configuration.

    Returns:
        list: A collection of initialized Button instances.
    '''
    buttons = []
    for button_cfg in buttons_cfg:
        buttons.append(Button(display_cfg=display_cfg, button_cfg=button_cfg))
    return buttons


def images_loader(display_cfg: dict, images_cfg: dict) -> list:
    '''
    Parses image configuration data to instantiate UI Image objects.

    Args:
        display_cfg (dict): Global display and asset settings.
        images_cfg (dict): Nested dictionary containing images configuration.

    Returns:
        list: A collection of initialized Text instances.
    '''
    images = []
    for image_cfg in images_cfg:
        images.append(Image(display_cfg=display_cfg, image_cfg=image_cfg))
    return images


def texts_loader(display_cfg: dict, texts_cfg: dict) -> list:
    '''
    Parses text configuration data to instantiate UI Text objects.

    Args:
        display_cfg (dict): Global display and asset settings.
        texts_cfg (dict): Nested dictionary containing texts configuration.

    Returns:
        list: A collection of initialized Text instances.
    '''
    texts = []
    for text_cfg in texts_cfg:
        texts.append(Text(display_cfg=display_cfg, text_cfg=text_cfg))
    return texts


def fonts_loader(display_cfg: dict) -> dict:
    '''
    Resolves filesystem paths and initializes Pygame font assets.
    Configuration dictionary contains the 'fonts' key.
    The 'fonts' is a mapping of font keys to file names and point sizes.

    Args:
        display_cfg (dict): Global display and asset settings.

    Returns:
        dict: A dictionary where keys match config and values are 
              pygame.font.Font objects.
    '''
    fonts_path = display_cfg['paths']['fonts']

    fonts = {}
    for key, data in display_cfg['fonts'].items():
        path = fonts_path / data['file']
        fonts[key] = pygame.font.Font(str(path), data['size'])
        
    return fonts


if __name__ == '__main__':
    pass