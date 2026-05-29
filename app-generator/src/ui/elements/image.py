import pygame
from typing import Optional


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


class Image:
    '''
    A class to represent and render a static image in Pygame.

    Attributes:
        path_image:
        image (pygame.Surface): The optimized image surface.
        size:
        width:
        height:
        rect (pygame.Rect): The rectangular area of the image for positioning.
    '''

    def __init__(self, display_cfg: dict, image_cfg: dict):
        '''
        Initializes the Image object by loading and optimizing the file.

        Args:
            display_cfg (dict): Global config containing asset paths.
            image_cfg (dict): Specific config with filename and coordinates.
        '''
        self.id = image_cfg['id']

        path_dir = display_cfg['paths']['images']
        self.path_image = path_dir / image_cfg['file']
        self.size = image_cfg.get('size', '')
        self.x = image_cfg['position']['x']
        self.y = image_cfg['position']['y']
        self.width = self.size['width']
        self.height = self.size['height']

        self.rotation = image_cfg.get('rotation')
        self.angle = 0

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.raw_img = pygame.image.load(str(self.path_image)).convert_alpha()
        self.raw_img = pygame.transform.smoothscale(self.raw_img, 
                                                    (self.width, self.height))
        
        self.curr_img = self.raw_img.copy()
        tint_color = image_cfg.get('tint_color')

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
        #screen.blit(self.curr_img, self.rect)

        if self.rotation:
            self.angle = (self.angle - 5) % 360
            center_x = self.x + self.width // 2
            center_y = self.y + self.height // 2
            
            rotated_image = pygame.transform.rotate(self.curr_img, self.angle)
            rect = rotated_image.get_rect(center=(center_x, center_y))
            screen.blit(rotated_image, rect.topleft)

        else:
            screen.blit(self.curr_img, self.rect)