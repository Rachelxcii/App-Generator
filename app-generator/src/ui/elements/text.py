import pygame
from typing import Optional


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


class Text:
        '''
        A class to manage and render static or dynamic text elements within a 
        Pygame surface.

        Attributes:
            text (str): The actual string content to be rendered.
            pos_x (int): The target X-coordinate for placement.
            pos_y (int): The target Y-coordinate for placement.
            font (pygame.font.Font): The Pygame font object used for rendering.
            color (tuple): RGB color tuple for the text surface.
        '''

        def __init__(self, display_cfg: dict, text_cfg: dict):
            '''
            Initializes the Text element by extracting content and styling 
            from configuration.

            Args:
                display_cfg (dict): Global configuration containing fonts and 
                                    color palettes.
                text_cfg (dict): Specific dictionary defining the text content,
                                 position, font key and color key.
            '''
            self.id = text_cfg['id']
            
            self.text = text_cfg['text']
            self.x = text_cfg['position']['x']
            self.y = text_cfg['position']['y']
            self.font = display_cfg['fonts'][text_cfg['font']]
            self.color = display_cfg['colors'][text_cfg['color']]
            
            self.size_cfg = display_cfg.get('size', '')
            self._prepare_surface()
        
        def _prepare_surface(self):
            '''
            Generates final text surface.
            '''
            raw_surface = self.font.render(self.text, True, self.color)

            if self.size_cfg:
                width = self.size_cfg['width']
                height = self.size_cfg['height']
                self.rect = pygame.Rect(self.x, self.y, width, height)
                center = self.rect.center

                ratio_w = (self.rect.width * 0.9) / raw_surface.get_width()
                ratio_h = (self.rect.height * 0.9) / raw_surface.get_height()
                scale_factor = min(ratio_w, ratio_h)

                width = int(raw_surface.get_width() * scale_factor)
                height = int(raw_surface.get_height() * scale_factor)
                size = (width, height)

                self.surface = pygame.transform.smoothscale(raw_surface, size)
                self.draw_pos = self.surface.get_rect(center=center)

            else:
                self.surface = raw_surface
                self.draw_pos = (self.x, self.y)
            

        def draw(self, screen: pygame.Surface) -> None:
            '''
            Renders the text to a surface and draws it at the specified 
            coordinates.

            Args:
                screen (pygame.Surface): Surface where text will be blitted.

            Returns:
                None
            '''
            screen.blit(self.surface, self.draw_pos)