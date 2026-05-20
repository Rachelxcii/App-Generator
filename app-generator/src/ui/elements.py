import pygame


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
            images_path = display_cfg['paths']['images']
            base_path = images_path / button_cfg['image']['base']
            hover_path = images_path / button_cfg['image']['hover']
            self.image_base = pygame.image.load(base_path).convert_alpha()
            self.image_hover = pygame.image.load(hover_path).convert_alpha()
                    
        self.rect = pygame.Rect(x, y, width, height)
        self.redirection = button_cfg['redirection']
        self.functions = button_cfg['functions']


    def _type_detector(): #TO-DO: type detector, to classify in text or image
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
            
            if self.subtype == 'text': #TO-DO: bool "to_adjust"
                text_image = self.font.render(self.text, True, (255, 255, 255))

                if text_image.get_width() > self.rect.width:
                    new_width = self.rect.width - 10 
                    ratio = new_width / text_image.get_width()
                    new_height = int(text_image.get_height() * ratio)
                    
                    text_image = pygame.transform.smoothscale(text_image, (new_width, new_height))

                text_rect = text_image.get_rect(center=self.rect.center)
                screen.blit(text_image, text_rect)

            else:
                text_surface = self.font.render(self.text, True, (255, 255, 255))
                width = int(self.rect.width * 0.9)
                height = int(self.rect.height * 0.9)
                text_scaled = pygame.transform.smoothscale(text_surface,
                                                        (width, height))

                text_rect = text_scaled.get_rect(center=self.rect.center)
                screen.blit(text_scaled, text_rect)


        elif self.subtype == 'image':
            img_to_draw = self.image_hover if is_hovering else self.image_base
            
            img_rect = img_to_draw.get_rect(center=self.rect.center)
            screen.blit(img_to_draw, img_rect)

    
    def get_actions(self) -> dict:
        '''
        Returns a dict with infomation about what MUST happen if a button is 
        clicked.
        Returns:
            dict: A collection of action triggers containing:
                - "redirection" (str/None): ID of the screen to navigate to.
                - "functions" (list/str): Identifier(s) of logic to execute.
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
            self.text = text_cfg['text']
            self.pos_x = text_cfg['position']['x']
            self.pos_y = text_cfg['position']['y']
            self.font = display_cfg['fonts'][text_cfg['font']]
            self.color = display_cfg['colors'][text_cfg['color']]

        def draw(self, screen) -> None:
            '''
            Renders the text to a surface and draws it at the specified 
            coordinates.

            Args:
                screen (pygame.Surface): Surface where text will be blitted.

            Returns:
                None
            '''
            text_format = self.font.render(self.text, True, self.color)
            screen.blit(text_format, (self.pos_x, self.pos_y))

    