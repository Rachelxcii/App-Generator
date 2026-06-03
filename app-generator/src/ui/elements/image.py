import pygame


def images_loader(window_cfg: dict, images_cfg: dict) -> list:
    '''
    Parses image configuration data to instantiate UI Image objects.

    Args:
        window_cfg (dict): Global window and asset settings.
        images_cfg (dict): Nested dictionary containing images configuration.

    Returns:
        list: A collection of initialized Text instances.
    '''
    images = []
    for image_cfg in images_cfg:
        images.append(Image(window_cfg=window_cfg, image_cfg=image_cfg))
    return images


class Image:
    '''
    Represents and manages a static or animated (rotating) image element.

    This class handles asset loading, surface optimization, color tinting, 
    and real-time transformation logic for the UI.

    Attributes:
        id (str): Unique identifier for the element.
        path_image (Path): Absolute path to the image asset.
        size (dict): Original size constraints from configuration.
        rect (pygame.Rect): Collision and positioning area.
        raw_img (pygame.Surface): The base optimized surface (original colors).
        curr_img (pygame.Surface): The processed surface (tinted or modified).
        rotation (bool): Whether the image should rotate over time.
        angle (int): Current rotation angle in degrees.
    '''

    def __init__(self, window_cfg: dict, image_cfg: dict):
        '''
        Initializes the Image object by loading, scaling, and tinting the 
        asset.

        Args:
            window_cfg (dict): Global window settings containing paths and 
                                color palettes.
            image_cfg (dict): Specific element configuration 
                              (file, position, size, tint).
        '''
        self.id = image_cfg['id']

        path_dir = window_cfg['paths']['images']
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
            target_rgb = window_cfg['colors'].get(tint_color, (255, 255, 255))
            self._tint_image(target_rgb)


    def _tint_image(self, rgb_color: tuple) -> None:
        '''
        Applies a color multiply tint to the surface while preserving alpha 
        channels.

        Args:
            rgb_color (tuple): RGB values used for the color multiplication.
        '''
        tint_surf = pygame.Surface((self.width, self.height)).convert_alpha()
        tint_surf.fill(rgb_color)
        
        self.curr_img = self.raw_img.copy()
        flags = pygame.BLEND_RGBA_MULT
        self.curr_img.blit(tint_surf, (0, 0), special_flags=flags)


    def draw(self, screen: pygame.Surface) -> None:
        '''
        Renders the image onto the destination surface.
        Handling rotation if enabled.
        
        Args: 
            screen (pygame.Surface): Surface where text will be blitted.
        '''
        if self.rotation:
            self.angle = (self.angle - 5) % 360
            center_x = self.x + self.width // 2
            center_y = self.y + self.height // 2
            
            rotated_image = pygame.transform.rotate(self.curr_img, self.angle)
            rect = rotated_image.get_rect(center=(center_x, center_y))
            screen.blit(rotated_image, rect.topleft)

        else:
            screen.blit(self.curr_img, self.rect)
