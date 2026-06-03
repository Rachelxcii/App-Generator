import pygame
from typing import Optional

from src.ui.elements.image import Image


def buttons_loader(window_cfg: dict, buttons_cfg: dict) -> list:
    '''
    Parses button configuration data to instantiate UI Button objects.

    Args:
        window_cfg (dict): Global window and asset settings.
        buttons_cfg (dict): Nested dictionary containing buttons configuration.

    Returns:
        list: A collection of initialized Button instances.
    '''
    buttons = []
    for button_cfg in buttons_cfg:
        buttons.append(Button(window_cfg=window_cfg, button_cfg=button_cfg))
    return buttons


class Button:
    '''
    A class to represent an interactive UI button in Pygame, supporting 
    both text-based and image-based rendering.

    Attributes:
        subtype (str): The type of button ('text' or 'image').
        rect (pygame.Rect): The rectangular collision and boundary area.
        text (str, optional): The label displayed on the button.
        color_base (tuple): RGB color for the default state.
        color_hover (tuple): RGB color for the hover state.
        color_curr (tuple): The current active RGB color.
        font (pygame.font.Font): The font object used for text rendering.
        image_base (pygame.Surface, optional): The default button image.
        image_hover (pygame.Surface, optional): The image displayed on hover.
        func_name (str): Identifier for the function to execute on click.
    '''

    def __init__(self, window_cfg: dict, button_cfg: dict):
        '''
        Initializes the Button by extracting layout, styling and assets 
        from configuration dictionaries.

        Args:
            window_cfg (dict): Global configuration containing fonts and 
                                color palettes.
            button_cfg (dict): Specific dictionary with position, size, subtype 
                               and functional data for this button.
        '''
        self.id = button_cfg['id']
        self.subtype = button_cfg['subtype']
        self.window_cfg = window_cfg
        self.button_cfg = button_cfg

        x = button_cfg['position']['x']
        y = button_cfg['position']['y']
        self.width = button_cfg['size']['width']
        self.height = button_cfg['size']['height']

        self.redirection = button_cfg.get('redirection', '')
        self.functions = button_cfg.get('functions', '')
        self.inputs = button_cfg.get('inputs', '')
        self.outputs = button_cfg.get('outputs', '')

        self.rect = pygame.Rect(x, y, self.width, self.height)
        self._subtype_attr_loader()


    def _subtype_attr_loader(self) -> None:
        '''
        Loads mandatory attributes depending on the subtype button.
        '''
        fonts = self.window_cfg['fonts']
        colors = self.window_cfg['colors']
        
        if self.subtype == 'text':
            self.text = self.button_cfg['text']
            self.font = fonts[self.button_cfg['font']]
            self.color_base = colors[self.button_cfg['color']['base']]
            self.color_hover = colors[self.button_cfg['color']['hover']]
            self.color_curr = colors[self.button_cfg['color']['base']]
            self._transform_text()
            
        elif self.subtype == 'image':
            img_base_cfg = self._get_image_cfg(mode_key='base')
            img_hover_cfg = self._get_image_cfg(mode_key='hover')

            self.img_base =  Image(window_cfg=self.window_cfg, 
                                   image_cfg=img_base_cfg)
            self.img_hover = Image(window_cfg=self.window_cfg, 
                                   image_cfg=img_hover_cfg)
            
    
    def _get_image_cfg(self, mode_key: str) -> dict:
        '''
        Extracts and merges visual parameters for a specific button state.
        Button state must be: base or hover.

        Returns:
            dict: Specific configuration depending on the button state.
        '''
        image_cfg = {}

        for param_key in self.button_cfg.keys():
            param = self.button_cfg.get(param_key)
            if isinstance(param, dict):
                subparam = param.get(mode_key, None)
                if subparam is not None:
                    image_cfg[param_key] = subparam
                    continue

            image_cfg[param_key] = param

        image_cfg['id'] = image_cfg['id'] + '_' + mode_key

        return image_cfg


    def _transform_text(self) -> None:
        '''
        Transforms text to fit the button size.

        Returns:
            None
        '''
        raw_text = self.font.render(self.text, True, (255, 255, 255))
    
        if raw_text.get_width() > self.rect.width:
            new_width = self.rect.width - 10 
            ratio = new_width / raw_text.get_width()
            new_height = int(raw_text.get_height() * ratio)
            self.text_surface = pygame.transform.smoothscale(raw_text, 
                                                                (new_width, 
                                                                new_height))
        else:
            self.text_surface = raw_text

        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    
    def get_actions(self) -> dict:
        '''
        Returns a dict with infomation about what MUST happen if a button is 
        clicked.

        Returns:
            dict: A collection of action triggers containing:
                - 'redirection' (str/None): ID of the screen to navigate to.
                - 'functions' (list/str): Identifier(s) of logic to execute.
                - 'inputs' (list/str): Identifier(s) of required inputs.
        '''
        return {
            'redirection': self.redirection,
            'functions': self.functions,
            'inputs': self.inputs,
            'outputs': self.outputs
        }
    

    def handle_events(self, event: pygame.event.Event) -> Optional[dict]:
        '''
        Processes internal button logic: hover states and click detection.
        
        Returns:
            dict: The actions (functions and redirection) if clicked, 
                  else None.
        '''
        pos_mouse = pygame.mouse.get_pos()
        self.is_hovering = self.rect.collidepoint(pos_mouse)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 1: left clic
                if self.is_hovering:
                    return self.get_actions()
        
        return None
                

    def draw(self, screen: pygame.Surface) -> None:
        '''
        Handles the rendering of the button and the hover logic.

        Args:
            screen (pygame.Surface): Surface where the button will be drawn.
        '''
        pos_mouse = pygame.mouse.get_pos()
        is_hovering = self.rect.collidepoint(pos_mouse)

        if self.subtype == 'text':
            color_curr = self.color_hover if is_hovering else self.color_base
            pygame.draw.rect(screen, color_curr, self.rect, border_radius=8)
            screen.blit(self.text_surface, self.text_rect)

        elif self.subtype == 'image':
        
            if is_hovering:
                self.img_hover.draw(screen)
            else:
                self.img_base.draw(screen)
