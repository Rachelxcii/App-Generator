import pygame
from typing import Optional
from src.ui.elements.image import Image


def loading_icons_loader(display_cfg: dict, loading_icons_cfg: dict, 
                         funcs_registry: dict) -> list:
    '''
    Parses configuration data to instantiate UI Loading Icon objects.

    Args:
        display_cfg (dict): Global display and asset settings.
        text_inputs (dict): Nested dictionary containing loading icons
                            configuration.

    Returns:
        list: A collection of initialized TextInput instances.
    '''
    loading_icons = []
    for loading_icon_cfg in loading_icons_cfg:
        loading_icons.append(LoadingIcon(display_cfg=display_cfg,
                                         loading_icon_cfg=loading_icon_cfg))
    return loading_icons


class LoadingIcon:
    '''
    WIP
    '''

    def __init__(self, display_cfg: dict, loading_icon_cfg: dict):
        '''

        functions_registry: internal_functions_registry and 
        external_functions_registry from screen_renderer.py

        '''
        self.id = loading_icon_cfg['id']
        self.display_cfg = display_cfg
        self.loading_icon_cfg = loading_icon_cfg

        self.func = loading_icon_cfg['monitored_function']
        self.is_running = False

        self._load_image(display_cfg=display_cfg,
                         loading_icon_cfg=loading_icon_cfg)


    def _load_image(self, display_cfg: dict, loading_icon_cfg: dict):

        image_cfg = {'id': loading_icon_cfg['id'], 
                     'type': 'image', 
                     'file': loading_icon_cfg['file'],
                     'position': loading_icon_cfg['position'],
                     'size': loading_icon_cfg['size'],
                     'tint_color': loading_icon_cfg.get('tint_color', {}),
                     'rotation': loading_icon_cfg.get('rotation', False)}
        
        self.image =  Image(display_cfg=display_cfg, 
                            image_cfg=image_cfg)


    def draw(self, screen: pygame.Surface) -> None:
        '''
        Loads and renders the image to the destination surface.
        
        Args:
            screen (pygame.Surface): Surface where text will be blitted.

        Returns:
            None
        '''
        if self.is_running:
            self.image.draw(screen)
