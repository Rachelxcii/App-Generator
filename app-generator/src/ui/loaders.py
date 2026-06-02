import pygame
from collections import defaultdict

from src.ui.elements.button import buttons_loader
from src.ui.elements.image import images_loader
from src.ui.elements.loading_icon import loading_icons_loader
from src.ui.elements.text import texts_loader
from src.ui.elements.text_input import text_inputs_loader
from src.ui.elements.text_output import text_outputs_loader


def element_detector(
        display_cfg: dict, elements_cfg: dict, funcs_registry: dict
        ) -> list:
    '''
    Orchestrates the identification and instantiation of UI components from raw data.

    This function acts as a central factory. It categorizes elements by type using 
    a grouping strategy (defaultdict) and delegates instantiation to specialized 
    loaders. This ensures that the main renderer receives a unified list of 
    ready-to-draw objects.

    Args:
        display_cfg (dict): Global engine configuration (paths, colors, fonts).
        elements_cfg (dict): Raw dictionary from JSON containing UI element schemas.
        funcs_registry (dict): Dictionary mapping function names to executable logic 
                               for interactive components (e.g., LoadingIcon).

    Returns:
        list: A flattened list of initialized UI component instances.
    '''
    # Group elements by type to process them with their specific loaders
    categories = defaultdict(list)

    for id, el_cfg in elements_cfg.items():
        el_cfg['id'] = id
        categories[el_cfg.get('type', 'unknown')].append(el_cfg)

    # Extract specific configurations for batch loading
    buttons_cfg = categories.get('button', '')
    images_cfg = categories.get('image', '')
    texts_cfg = categories.get('text', '')
    text_inputs_cfg = categories.get('text_input', '')
    text_outputs_cfg = categories.get('text_output', '')
    loading_icons_cfg = categories.get('loading_icon', '')

    elements = []

    # Batch processing via specialized loaders
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

    if text_outputs_cfg:
        text_outputs = text_outputs_loader(display_cfg=display_cfg, 
                                           text_outputs_cfg=text_outputs_cfg)
        elements += text_outputs

    if loading_icons_cfg:
        # LoadingIcons require funcs_registry to monitor Worker Thread state
        loading_icons = loading_icons_loader(
            display_cfg=display_cfg,
            loading_icons_cfg=loading_icons_cfg,
            #funcs_registry=funcs_registry
            )
        elements += loading_icons
    
    return elements
    

def fonts_loader(display_cfg: dict) -> dict:
    '''
    Resolves filesystem paths and initializes Pygame font assets.

    Parses the 'fonts' section of the configuration to map font keys to 
    instantiated pygame.font.Font objects using the provided system paths.

    Args:
        display_cfg (dict): Global display and asset settings.

    Returns:
        dict: Mapping of font identifiers (str) to pygame.font.Font objects.
    '''
    fonts_path = display_cfg['paths']['fonts']

    fonts = {}
    for key, data in display_cfg['fonts'].items():
        path = fonts_path / data['file']
        fonts[key] = pygame.font.Font(str(path), data['size'])
        
    return fonts
