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
        self._subtype_attr_loader(display_cfg=display_cfg, button_cfg=button_cfg)

        x = button_cfg['position']['x']
        y = button_cfg['position']['y']
        width = button_cfg['size']['width']
        height = button_cfg['size']['height']

        self.rect = pygame.Rect(x, y, width, height)
        self.redirection = button_cfg['redirection']
        self.functions = button_cfg['functions']


    def _subtype_attr_loader(self, display_cfg: dict, button_cfg: dict):
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


    def tint_image(self, rgb_color: tuple):
        '''
        Applies a color tint to the image while preserving transparency.
        '''
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

            # TO-DO: Keep raw image size
            # img_rect = img_to_draw.get_rect(center=self.rect.center)
            # screen.blit(img_to_draw, img_rect)

            # Scale the image to fit the rect
            # TO-DO: Adjust the image to fit the rect, when image is bigger than rect
            img_scaled = pygame.transform.smoothscale(img_to_draw, (self.rect.width, self.rect.height))
            screen.blit(img_scaled, self.rect)

    
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
    

class Image:  # TO-DO: duda sobre draw, este method se ejecutara cada refresco de la screen o solo una vez???
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
        path_dir = display_cfg['paths']['images']
        self.path_image = path_dir / image_cfg['file']
        self.size = image_cfg.get('size', '')
        x = image_cfg['position']['x']
        y = image_cfg['position']['y']
        self.width = self.size['width']
        self.height = self.size['height']

        self.rect = pygame.Rect(x, y, self.width, self.height)

        self.raw_img = pygame.image.load(str(self.path_image)).convert_alpha()
        self.raw_img = pygame.transform.smoothscale(self.raw_img, 
                                                    (self.width, self.height))
        
        self.curr_img = self.raw_img.copy()
        tint_color = image_cfg.get('tint_color')

        if tint_color:
            target_rgb = display_cfg['colors'].get(tint_color, (255, 255, 255))
            self.tint_image(target_rgb)


    def tint_image(self, rgb_color: tuple):
        '''
        Applies a color tint to the image while preserving transparency.
        '''
        tint_surf = pygame.Surface((self.width, self.height)).convert_alpha()
        tint_surf.fill(rgb_color)
        
        self.curr_img = self.raw_img.copy()
        
        # BLEND_RGBA_MULT multiply the colors
        self.curr_img.blit(tint_surf, (0, 0),
                           special_flags=pygame.BLEND_RGBA_MULT)


    def draw(self, screen: pygame.Surface) -> None:
        '''Loads and renders the image to the destination surface.
        
        Args:
            screen (pygame.Surface): Surface where text will be blitted.

        Returns:
            None
        '''
        screen.blit(self.curr_img, self.rect)


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
            self.x = text_cfg['position']['x']
            self.y = text_cfg['position']['y']
            self.font = display_cfg['fonts'][text_cfg['font']]
            self.color = display_cfg['colors'][text_cfg['color']]
            
            self.size = display_cfg.get('size', "")

            print(f'SIZE: {self.size}')

            if self.size:
                width = display_cfg['size']['width']
                height = display_cfg['size']['height']
                self.rect = pygame.Rect(self.x, self.y, width, height)


        def draw(self, screen: pygame.Surface) -> None:
            '''
            Renders the text to a surface and draws it at the specified 
            coordinates.

            Args:
                screen (pygame.Surface): Surface where text will be blitted.

            Returns:
                None
            '''
            if self.size:

                print(f'--- {self.text} HAS SIZE ---')

                text_surface = self.font.render(self.text, True, self.color)

                ratio_w = (self.rect.width * 0.9) / text_surface.get_width()
                ratio_h = (self.rect.height * 0.9) / text_surface.get_height()
                scale_factor = min(ratio_w, ratio_h)
                width = int(text_surface.get_width() * scale_factor)
                height = int(text_surface.get_height() * scale_factor)
                new_size = (width,height)

                size = (int(text_surface.get_width()), int(text_surface.get_height()))
                text_scaled = pygame.transform.smoothscale(text_surface, size)

                text_rect = text_scaled.get_rect(center=self.rect.center)
                screen.blit(text_scaled, text_rect)

            else:
                #print(f'--- {self.text} HAS NO SIZE ---')
                text_format = self.font.render(self.text, True, self.color)
                screen.blit(text_format, (self.x, self.y))


class TextInput:
    '''
    Managed UI element for text entry, handling focus, keyboard input, and 
    rendering.
    
    Attributes:
        text (str): The current string entered by the user.
        active (bool): Whether the element is focused and capturing keystrokes.
        rect (pygame.Rect): The collision and drawing area.
        color_active (tuple): Border color when focused.
        color_passive (tuple): Border color when idle.
    '''

    def __init__(self, display_cfg: dict, text_input_cfg: dict):
        '''
        Initializes the Input field with styling and positioning.
        '''
        self.rect = pygame.Rect(text_input_cfg['position']['x'], 
                                text_input_cfg['position']['y'], 
                                text_input_cfg['size']['width'], 
                                text_input_cfg['size']['height'])
        
        self.colors = display_cfg['colors']
        self.font = display_cfg['fonts'][text_input_cfg.get('font', 'default')]
        
        self.text = ""
        self.active = False
        
        self.color_active = self.colors.get(text_input_cfg.get('color_active'), 
                                            (255, 255, 255))
        self.color_passive = self.colors.get(text_input_cfg.get('color_passive'), 
                                             (100, 100, 100))
        self.color_curr = self.color_passive

    def handle_events(self, event: pygame.event.Event) -> None:
        '''
        Manages focus toggling and keyboard capture.
        '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle focus if user clicks the box
            self.active = self.rect.collidepoint(event.pos)
            self.color_curr = self.color_active if self.active else self.color_passive

        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False  # Finish input
                self.color_curr = self.color_passive
            else:
                # Limit text length to avoid overflow (optional logic)
                if len(self.text) < 20: 
                    self.text += event.unicode

    def draw(self, screen: pygame.Surface) -> None:
        '''Renders the input box and the current text.'''
        # 1. Draw the background/border
        pygame.draw.rect(screen, self.color_curr, self.rect, 2)
        
        # 2. Render the text
        text_surface = self.font.render(self.text, True, self.colors.get('text', (255, 255, 255)))
        
        # 3. Blit with a small padding
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + (self.rect.height // 4)))
    