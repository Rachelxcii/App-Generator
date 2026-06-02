import pygame


def text_inputs_loader(display_cfg: dict, text_inputs_cfg: dict) -> list:
    '''
    Parses text configuration data to instantiate UI Text objects.

    Args:
        display_cfg (dict): Global display and asset settings.
        text_inputs (dict): Nested dictionary containing text inputs 
                            configuration.

    Returns:
        list: A collection of initialized TextInput instances.
    '''
    text_inputs = []
    for text_input_cfg in text_inputs_cfg:
        text_inputs.append(TextInput(display_cfg=display_cfg, 
                                     text_input_cfg=text_input_cfg))
    return text_inputs


class TextInput:
    '''
    A reactive UI element for text entry, supporting focus management,
    keyboard input handling, and dynamic text rendering.

    Attributes:
        id (str): Unique identifier for the input field.
        text (str): The current string entered by the user.
        active (bool): Whether the element is focused and capturing input.
        rect (pygame.Rect): The bounding box for collision and rendering.
        color_active (tuple): Border color when focused.
        color_passive (tuple): Border color when idle.
        showing_placeholder (bool): State flag for placeholder visibility.
    '''

    def __init__(self, display_cfg: dict, text_input_cfg: dict):
        '''
        Initializes the Input field with styling and positioning.

        Args:
            display_cfg (dict): Global display/theme configuration.
            text_input_cfg (dict): Specific configuration for this instance.
        '''
        self.id = text_input_cfg['id']

        self.text_input_cfg = text_input_cfg
        self.rect = pygame.Rect(text_input_cfg['position']['x'], 
                                text_input_cfg['position']['y'], 
                                text_input_cfg['size']['width'], 
                                text_input_cfg['size']['height']) 
        
        self.colors = display_cfg['colors']
        self.font = display_cfg['fonts'][text_input_cfg.get('font', 'default')]
        pygame.key.set_repeat(500, 50)
        
        # Initial state
        self.placeholder = text_input_cfg.get('placeholder', '')
        self.text = self.placeholder
        self.active = False
        self.showing_placeholder = True
        
        #Colors
        self.color_active = self.colors.get(
            text_input_cfg.get('active_color'), (255, 255, 255)
            )
        self.color_passive = self.colors.get(
            text_input_cfg.get('passive_color'), (100, 100, 100)
            )
        self.color_curr = self.color_passive
        self.color_text = self.colors.get('text', (255, 255, 255))
        self.color_placeholder = (150, 150, 150)

        # Initial render
        self._update_surface()
    

    def _update_surface(self):
        '''
        Renders the current text or placeholder to an optimized surface.
        '''
        color = (
            self.color_placeholder if self.showing_placeholder 
            else self.color_text
            )
        display_text = self.text if self.text != "" else " "
        self.text_surface = self.font.render(display_text, True, color)
        

    def handle_events(self, event: pygame.event.Event) -> None:
        '''
        Manages focus toggling via mouse and keyboard input processing.

        Args:
            event (pygame.event.Event): The current Pygame event to process.
        '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            
            if self.active:
                pygame.key.start_text_input()
                if self.showing_placeholder:
                    # If it's the first time the user clicks inside the box, 
                    # the placeholder is still visible.
                    self.text = ""
                    self.showing_placeholder = False
                    self._update_surface()
            else:
                if self.text == "":
                    # If user clicks outside the box and there is no text,
                    # the placeholder is restored.
                    self.text = self.placeholder
                    self.showing_placeholder = True
                    self._update_surface()

            self.color_curr = (self.color_active if self.active
                               else self.color_passive)            

        # --- KEYBOARD INPUT LOGIC ---
        if self.active and event.type == pygame.KEYDOWN:

            if event.key == pygame.K_BACKSPACE:

                if not self.showing_placeholder and len(self.text) > 0:
                    self.text = self.text[:-1]

                    if self.text == "":
                        self.text = self.placeholder
                        self.showing_placeholder = True
                    
                    self._update_surface()

            elif event.key == pygame.K_RETURN:
                if self.text_input_cfg.get('allow_multiline', False):
                    self.text += "\n"
                    self._update_surface()
                else:
                    self.active = False
                    self.color_curr = self.color_passive
                    pygame.key.stop_text_input()

            else:
                if event.unicode.isprintable() and event.unicode != "":

                    if self.showing_placeholder:
                        self.text = ""
                        self.showing_placeholder = False
                    
                    if len(self.text) < self.text_input_cfg.get(
                        'max_chars', 1000
                    ): 
                        self.text += event.unicode
            
            self._update_surface()


    def draw(self, screen: pygame.Surface) -> None:
        '''
        Renders the input box, applies clipping for overflow and 
        draws the text.

        Args:
            screen (pygame.Surface): The display surface to draw on.
        '''
        # Draws the edges of the box
        pygame.draw.rect(screen, self.color_curr, self.rect, 2)
        
        # Applies clipping to ensure text doesn't bleed outside the box
        clip_rect = self.rect.inflate(-4, -4) 
        old_clip = screen.get_clip()
        screen.set_clip(clip_rect)
        
        # Horizontal scroll logic: align text to the right if it exceeds width
        text_width = self.text_surface.get_width()
        max_width = self.rect.width - 10
        
        offset_x = 0
        if text_width > max_width:
            offset_x = max_width - text_width

        # Draws text centered vertically with calculated offset
        text_pos = (self.rect.x + 5 + offset_x,
                    self.rect.centery - (self.text_surface.get_height() // 2))
        screen.blit(self.text_surface, text_pos)
        
        # Restores original clipping area
        screen.set_clip(old_clip)