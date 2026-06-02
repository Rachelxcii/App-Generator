import pygame


def text_outputs_loader(display_cfg: dict, text_outputs_cfg: dict) -> list:
    '''
    Parses text configuration data to instantiate UI TextOutput objects.

    Args:
        display_cfg (dict): Global display and asset settings.
        text_outputs_cfg (dict): Nested dictionary containing text outputs 
                                 configuration.

    Returns:
        list: A collection of initialized TextOuput instances.
    '''
    text_outputs = []
    for text_output_cfg in text_outputs_cfg:
        text_outputs.append(TextOutput(display_cfg=display_cfg, 
                                       text_output_cfg=text_output_cfg))
    return text_outputs


class TextOutput:
    '''
    A dynamic UI element used to display data-driven results.

    Unlike the static Text class, TextOutput allows for real-time updates of 
    its content while maintaining the architectural constraints (scaling, 
    centering, and styling) defined in the JSON schema.

    Attributes:
        id (str): Unique identifier for data binding.
        text (str): The current string value to display.
        font (pygame.font.Font): The resolved font asset.
        color (tuple): RGB color for the text.
    '''

    def __init__(self, display_cfg: dict, text_output_cfg: dict):
        '''
        Initializes the output field with its configuration schema.
        '''
        self.id = text_output_cfg['id']
        self.subtype = text_output_cfg['subtype']
        self.display_cfg = display_cfg
        self.text_output_cfg = text_output_cfg

        self.monitored_functions = text_output_cfg.get('monitored_functions')

        self.font = display_cfg['fonts'][text_output_cfg['font']]
        self.color = display_cfg['colors'][text_output_cfg['color']]
        
        self.text = text_output_cfg.get('initial_text', ' ')
        
        self.x = text_output_cfg['position']['x']
        self.y = text_output_cfg['position']['y']
        
        self.size_cfg = text_output_cfg.get('size')
        
        self.update_content(self.text)


    def update_content(self, new_text: any) -> None:
        '''
        Updates the displayed string and recalculates the scaled surface.

        This method is the primary entry point for the Worker Thread or 
        Screen Controller to push new data to the UI.

        Args:
            new_text (str): The new string to be rendered.
        '''
        self.text = str(new_text)
        self._prepare_surface()


    def _prepare_surface(self) -> None:
        '''
        Renders and scales the text surface, following the 'Text' class logic.
        Ensures the text fits within the bounding box if provided.
        '''
        # Render high-quality base text
        raw_surface = self.font.render(self.text, True, self.color)

        if self.size_cfg:
            width_max = self.size_cfg['width']
            height_max = self.size_cfg['height']
            self.rect = pygame.Rect(self.x, self.y, width_max, height_max)
            center = self.rect.center

            # Calculate scaling to fit 90% of the container
            # Preventing division by zero for empty strings
            src_w = max(raw_surface.get_width(), 1)
            src_h = max(raw_surface.get_height(), 1)
            
            ratio_w = (self.rect.width * 0.9) / src_w
            ratio_h = (self.rect.height * 0.9) / src_h
            scale_factor = min(ratio_w, ratio_h)

            new_size = (int(src_w * scale_factor), int(src_h * scale_factor))

            self.surface = pygame.transform.smoothscale(raw_surface, new_size)
            self.draw_pos = self.surface.get_rect(center=center)

        else:
            self.surface = raw_surface
            self.draw_pos = (self.x, self.y)


    def draw(self, screen: pygame.Surface) -> None:
        '''
        Blits the current output surface to the screen.

        Args:
            screen (pygame.Surface): The display surface to draw on.
        '''
        screen.blit(self.surface, self.draw_pos)
