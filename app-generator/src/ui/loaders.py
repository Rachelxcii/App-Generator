import pygame
from collections import defaultdict

from src.ui.elements.button import buttons_loader
from src.ui.elements.image import images_loader
from src.ui.elements.loading_icon import loading_icons_loader
from src.ui.elements.text import texts_loader
from src.ui.elements.text_input import text_inputs_loader


def element_detector(display_cfg: dict, elements_cfg: dict, funcs_registry: dict) -> list:
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

    buttons_cfg = categories.get('button', '')
    images_cfg = categories.get('image', '')
    texts_cfg = categories.get('text', '')
    text_inputs_cfg = categories.get('text_input', '')
    loading_icons_cfg = categories.get('loading_icon', '')

    elements = []

    if buttons_cfg:
        buttons = buttons_loader(display_cfg=display_cfg, 
                                 buttons_cfg=buttons_cfg)
        elements += buttons
        
    if images_cfg:
        images = images_loader(display_cfg=display_cfg, images_cfg=images_cfg)
        elements += images
    
    if texts_cfg:
        texts = texts_loader(display_cfg=display_cfg, texts_cfg=texts_cfg)
        elements += texts

    if text_inputs_cfg:
        text_inputs = text_inputs_loader(display_cfg=display_cfg, 
                                         text_inputs_cfg=text_inputs_cfg)
        elements += text_inputs

    if loading_icons_cfg:
        loading_icons = loading_icons_loader(display_cfg=display_cfg, 
                                             loading_icons_cfg=loading_icons_cfg,
                                             funcs_registry=funcs_registry)
        elements += loading_icons
    
    return elements
    

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