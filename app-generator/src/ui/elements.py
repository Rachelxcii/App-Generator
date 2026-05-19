import pygame


class Button:
    '''
    A class to represent an interactive UI button in Pygame.

    Attributes:
        rect (pygame.Rect): The rectangular area of the button.
        text (str): The label displayed on the button.
        color_base (tuple): RGB color of the button in its default state.
        color_hover (tuple): RGB color of the button when the mouse is over it.
        color_curr (tuple): The current active color of the button.
        button_font (pygame.font.Font): The font object used to render the text.
    '''

    def __init__(self, display_cfg: dict, button_cfg: dict):
        '''
        Initializes the Button with coordinates, dimensions, and styling.

        Args:
            x (int): X-coordinate of the top-left corner.
            y (int): Y-coordinate of the top-left corner.
            width (int): Width of the button.
            height (int): Height of the button.
            text (str): Text to be displayed on the button.
            color_base (tuple): Default RGB color.
            color_hover (tuple): Hover RGB color.
        '''
        self.subtype = button_cfg['subtype']
        x = button_cfg['position']['x']
        y = button_cfg['position']['y']
        width = button_cfg['size']['width']
        height = button_cfg['size']['height']
        fonts = display_cfg['fonts']
        colors = display_cfg['colors']

        if self.subtype == 'text':
            self.text = button_cfg['text']
            self.font = fonts[button_cfg['font']]
            self.color_base = colors[button_cfg['color']['base']]
            self.color_hover = colors[button_cfg['color']['hover']]
            self.color_curr = colors[button_cfg['color']['base']]
            
        elif self.subtype == 'image':
            images_path = display_cfg['paths']['images_dir']
            base_path = images_path / button_cfg['image']['base']
            hover_path = images_path / button_cfg['image']['hover']

            self.image_base = pygame.image.load(base_path).convert_alpha()
            self.image_hover = pygame.image.load(hover_path).convert_alpha()
            
        
        print(f'BUTTON CONFIG: {button_cfg}')
        
        self.rect = pygame.Rect(x, y, width, height)

        self.redirection = button_cfg['redirection']
        self.functions = button_cfg['functions']


    def _type_detector():
        pass


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
            
            text_image = self.font.render(self.text, True, (255, 255, 255))
            text_rect = text_image.get_rect(center=self.rect.center)
            screen.blit(text_image, text_rect)

        elif self.subtype == 'image':
            img_to_draw = self.image_hover if is_hovering else self.image_base
            
            img_rect = img_to_draw.get_rect(center=self.rect.center)
            screen.blit(img_to_draw, img_rect)

        '''# Change button color when hovering
        pos_mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos_mouse):
            self.color_curr = self.color_hover
        else:
            self.color_curr = self.color_base

        # Draw button rectangle, for collisions
        pygame.draw.rect(screen, self.color_curr, self.rect, border_radius=8)
        
        # Render centered text
        text_image = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_image.get_rect(center=self.rect.center)
        screen.blit(text_image, text_rect)'''

    
    def get_actions(self) -> dict:
        '''
        Returns a dict with infomation about what MUST happen if a button is 
        clicked.
        '''
        return {
            "redirection": self.redirection,
            "functions": self.functions
        }


    def button_clicked(self, event: pygame.event.Event) -> bool:
        '''
        Checks if the left mouse button was clicked within the button's area.

        Args:
            event (pygame.event.Event): The Pygame event to be processed.

        Returns:
            bool: True if the button was clicked, False otherwise.
        '''

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class Text:
        '''
        A class to represent and render a static or dynamic title text in Pygame.

        Attributes:
            name (str): The text content to be displayed as a title.
            size (int): The font size (used for logical reference).
            pos_x (int): The initial X-coord, may be overridden by centering logic.
            pos_y (int): The Y-coord of the title.
            font (pygame.font.Font): The font object used for rendering.
            color (tuple): RGB color of the title text.
            win_width (int): Current width of the application window for centering.
            win_height (int): Current height of the application window.
        '''

        def __init__(self, display_cfg: dict, text_cfg: dict):
            '''
            Initializes the Title with text content, styling, and window context.

            Args:
                name (str): The string to display.
                size (int): Reference size of the font.
                pos_x (int): Targeted X position.
                pos_y (int): Targeted Y position.
                font (pygame.font.Font): Pre-loaded Pygame font object.
                color (tuple): RGB color tuple for the text.
                win_width (int): Window width used to calculate horizontal centering.
                win_height (int): Window height for vertical context.
            '''
            self.text = text_cfg['text']
            self.pos_x = text_cfg['position']['x']
            self.pos_y = text_cfg['position']['y']
            self.font = display_cfg['fonts'][text_cfg['font']]
            self.color = display_cfg['colors'][text_cfg['color']]

        def draw(self, screen) -> None:
            '''
            Renders title text and draws it centered horizontally on the screen.

            Args:
                screen (pygame.Surface): The surface where title will be blitted.

            Returns:
                None
            '''
            text_format = self.font.render(self.text, True, self.color)
            screen.blit(text_format, (self.pos_x, self.pos_y))

    