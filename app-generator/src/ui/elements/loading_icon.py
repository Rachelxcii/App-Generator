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

        self.x = loading_icon_cfg['position']['x']
        self.y = loading_icon_cfg['position']['y']
        self.width = loading_icon_cfg['size']['width']
        self.height = loading_icon_cfg['size']['height']
        self.pos = (self.x, self.y)
        self.monitored_func_name = loading_icon_cfg.get('monitored_function')
        path_dir = display_cfg['paths']['images']
        self.path_image = path_dir / loading_icon_cfg['image_or_gif']

        self.func = loading_icon_cfg['monitored_function']
        self.is_running = False
        self.rotation = loading_icon_cfg.get('rotation')
        self.angle = 0

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.raw_img = pygame.image.load(str(self.path_image)).convert_alpha()
        self.raw_img = pygame.transform.smoothscale(self.raw_img, 
                                                    (self.width, self.height))
        
        self.curr_img = self.raw_img.copy()
        tint_color = loading_icon_cfg.get('tint_color')

        if tint_color:
            target_rgb = display_cfg['colors'].get(tint_color, (255, 255, 255))
            self._tint_image(target_rgb)


    def _tint_image(self, rgb_color: tuple):
        '''
        Applies a color tint to the image while preserving transparency.
        '''
        tint_surf = pygame.Surface((self.width, self.height)).convert_alpha()
        tint_surf.fill(rgb_color)
        
        self.curr_img = self.raw_img.copy()
        flags = pygame.BLEND_RGBA_MULT
        self.curr_img.blit(tint_surf, (0, 0), special_flags=flags)


    def draw(self, screen: pygame.Surface) -> None:
        '''
        Loads and renders the image to the destination surface.
        
        Args:
            screen (pygame.Surface): Surface where text will be blitted.

        Returns:
            None
        '''
        if self.is_running:
            if self.rotation:
                self.angle = (self.angle - 5) % 360
                center_x = self.x + self.width // 2
                center_y = self.y + self.height // 2
                
                rotated_image = pygame.transform.rotate(self.curr_img, self.angle)
                rect = rotated_image.get_rect(center=(center_x, center_y))
                screen.blit(rotated_image, rect.topleft)

            else:
                screen.blit(self.curr_img, self.rect)