import pygame


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
        Represents a UI text element with support for automatic scaling and 
        positioning.

        This class handles the conversion of raw strings into optimized Pygame 
        surfaces. It includes logic to auto-fit text into a bounding box while 
        maintaining aspect ratio if a target size is provided.

        Attributes:
            id (str): Unique identifier for the element.
            text (str): The string content to be rendered.
            font (pygame.font.Font): The resolved font asset.
            color (tuple): RGB color used for the typeface.
            surface (pygame.Surface): Final rendered and scaled text surface.
            draw_pos (tuple/pygame.Rect): The final blit coordinates or Rect.
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
        
        
        def _prepare_surface(self) -> None:
            '''
            Generates the optimized text surface.

            If a 'size' configuration is present, it calculates a scale factor 
            to fit the text within a bounding box (90% padding) using 
            smoothscale transformations.
            Otherwise, it defaults to a standard blit.
            '''
            # Initial high-quality render
            raw_surface = self.font.render(self.text, True, self.color)

            if self.size_cfg:
                # Bounding box definition
                width = self.size_cfg['width']
                height = self.size_cfg['height']
                self.rect = pygame.Rect(self.x, self.y, width, height)
                center = self.rect.center

                # Aspect Ratio Calculation:
                # Ensures text fits within 90% of the box
                ratio_w = (self.rect.width * 0.9) / raw_surface.get_width()
                ratio_h = (self.rect.height * 0.9) / raw_surface.get_height()
                scale_factor = min(ratio_w, ratio_h)

                # Select the most restrictive ratio to avoid overflow
                width = int(raw_surface.get_width() * scale_factor)
                height = int(raw_surface.get_height() * scale_factor)
                size = (width, height)

                # Smooth transformation to avoid aliasing artifacts
                self.surface = pygame.transform.smoothscale(raw_surface, size)
                # Center the scaled surface within the original bounding box
                self.draw_pos = self.surface.get_rect(center=center)

            else:
                # Standard rendering without scaling constraints
                self.surface = raw_surface
                self.draw_pos = (self.x, self.y)
            

        def draw(self, screen: pygame.Surface) -> None:
            '''
            Renders the text to a surface and draws it at the specified 
            coordinates.

            Args:
                screen (pygame.Surface): Surface where text will be blitted.
            '''
            screen.blit(self.surface, self.draw_pos)