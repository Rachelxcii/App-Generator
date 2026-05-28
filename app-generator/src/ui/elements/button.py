import pygame
from typing import Optional


def buttons_loader(display_cfg: dict, buttons_cfg: dict) -> list:
    '''
    Parses button configuration data to instantiate UI Button objects.

    Args:
        display_cfg (dict): Global display and asset settings.
        buttons_cfg (dict): Nested dictionary containing buttons configuration.

    Returns:
        list: A collection of initialized Button instances.
    '''
    buttons = []
    for button_cfg in buttons_cfg:
        buttons.append(Button(display_cfg=display_cfg, button_cfg=button_cfg))
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

    def __init__(self, display_cfg: dict, button_cfg: dict):
        '''
        Initializes the Button by extracting layout, styling and assets 
        from configuration dictionaries.

        Args:
            display_cfg (dict): Global configuration containing fonts and 
                                color palettes.
            button_cfg (dict): Specific dictionary with position, size, subtype 
                               and functional data for this button.
        '''
        self.subtype = button_cfg['subtype']
        self.id = button_cfg['id']

        x = button_cfg['position']['x']
        y = button_cfg['position']['y']
        self.width = button_cfg['size']['width']
        self.height = button_cfg['size']['height']

        self.redirection = button_cfg.get('redirection', '')
        self.functions = button_cfg.get('functions', '')
        self.inputs = button_cfg.get('inputs', '')

        self.rect = pygame.Rect(x, y, self.width, self.height)
        self._subtype_attr_loader(display_cfg=display_cfg, button_cfg=button_cfg)


    def _subtype_attr_loader(self, display_cfg: dict, button_cfg: dict):
        '''
        Loads mandatory attributes depending on the subtype button.
        '''
        fonts = display_cfg['fonts']
        colors = display_cfg['colors']
        
        if self.subtype == 'text':
            self.text = button_cfg['text']
            self.font = fonts[button_cfg['font']]
            self.color_base = colors[button_cfg['color']['base']]
            self.color_hover = colors[button_cfg['color']['hover']]
            self.color_curr = colors[button_cfg['color']['base']]
            self._transform_text()
            
        elif self.subtype == 'image':
            images_path = display_cfg['paths']['images']
            base_path = images_path / button_cfg['image']['base']
            hover_path = images_path / button_cfg['image']['hover']

            raw_img_base = pygame.image.load(base_path).convert_alpha()
            raw_img_hover = pygame.image.load(hover_path).convert_alpha()

            self.img_base = pygame.transform.smoothscale(raw_img_base, 
                                                        self.rect.size)
            self.img_hover = pygame.transform.smoothscale(raw_img_hover, 
                                                          self.rect.size)

            self._apply_tints(display_cfg=display_cfg, button_cfg=button_cfg)


    def _transform_text(self):
        '''
        Transforms text to fit the button size.
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


    def _apply_tints(self, display_cfg: dict, button_cfg: dict):
        '''
        Applies a color tint to the image while preserving transparency.
        '''
        tint_cfg = button_cfg.get("tint_color")
        
        if tint_cfg.get('base'):
            color = display_cfg['colors'].get(tint_cfg['base'])
            self.img_base = self._execute_tint(surface=self.img_base, 
                                               color=color)

        if tint_cfg.get('hover'):
            color = display_cfg['colors'].get(tint_cfg['hover'])
            self.img_hover = self._execute_tint(surface=self.img_hover,
                                               color=color)


    def _execute_tint(self, surface: pygame.Surface, color: tuple) -> pygame.Surface:
        '''
        Helper to multiply a surface by a color.
        '''
        tint_surf = pygame.Surface((self.width, self.height)).convert_alpha()
        tint_surf.fill(color)
        
        result_img = surface.copy()
        flags = pygame.BLEND_RGBA_MULT
        result_img.blit(tint_surf, (0, 0), special_flags=flags)

        return result_img

    
    def get_actions(self) -> dict:
        '''
        Returns a dict with infomation about what MUST happen if a button is 
        clicked.
        Returns:
            dict: A collection of action triggers containing:
                - "redirection" (str/None): ID of the screen to navigate to.
                - "functions" (list/str): Identifier(s) of logic to execute.
        '''
        dict_ga = {
            "redirection": self.redirection,
            "functions": self.functions,
            "inputs": self.inputs
        }
        print(f'GET ACTION: {dict_ga}')
        return {
            "redirection": self.redirection,
            "functions": self.functions,
            "inputs": self.inputs
        }
    

    def handle_events(self, event: pygame.event.Event) -> Optional[dict]:
        '''
        Processes internal button logic: hover states and click detection.
        
        Returns:
            dict: The actions (functions and redirection) if clicked, else None.
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
            screen (pygame.Surface): The surface where the button will be drawn.

        Returns:
            None
        '''
        pos_mouse = pygame.mouse.get_pos()
        is_hovering = self.rect.collidepoint(pos_mouse)

        if self.subtype == 'text':
            self.color_curr = self.color_hover if is_hovering else self.color_base
            pygame.draw.rect(screen, self.color_curr, self.rect, border_radius=8)
            screen.blit(self.text_surface, self.text_rect)

        elif self.subtype == 'image':
            img = self.img_hover if is_hovering else self.img_base
            screen.blit(img, self.rect)