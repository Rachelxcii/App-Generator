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

    def __init__(self, x: int, y: int, weight: int, height: int, text: str, 
                 font: pygame.font.Font, color_base: tuple, color_hover: tuple,
                 action_data: dict):
        '''
        Initializes the Button with coordinates, dimensions, and styling.

        Args:
            x (int): X-coordinate of the top-left corner.
            y (int): Y-coordinate of the top-left corner.
            weight (int): Width of the button.
            height (int): Height of the button.
            text (str): Text to be displayed on the button.
            color_base (tuple): Default RGB color.
            color_hover (tuple): Hover RGB color.
        '''

        self.rect = pygame.Rect(x, y, weight, height)
        self.text = text
        self.color_base = color_base
        self.color_hover = color_hover
        self.color_curr = color_base
        self.button_font = font
        
        self.action_type = action_data.get("actions", [])
        self.redirection = action_data.get("redirection", "")
        self.functions = action_data.get("functions", [])


    def drawing(self, screen: pygame.Surface) -> None:
        '''
        Handles the rendering of the button and the hover logic.

        Args:
            screen (pygame.Surface): The surface where the button will be drawn.

        Returns:
            None
        '''

        # Change button color when hovering
        pos_mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos_mouse):
            self.color_curr = self.color_hover
        else:
            self.color_curr = self.color_base

        # Draw button rectangle, for collisions
        pygame.draw.rect(screen, self.color_curr, self.rect, border_radius=8)
        
        # Render centered text
        text_image = self.button_font.render(self.text, True, (255, 255, 255))
        text_rect = text_image.get_rect(center=self.rect.center)
        screen.blit(text_image, text_rect)

    
    def get_actions(self):
        '''
        Returns a dict with infomation about what MUST happen if a button is 
        clicked.
        '''
        return {
            "type": self.action_type,
            "goto": self.redirection,
            "call": self.functions
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
    

class Title:
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

    def __init__(self, name: str, size: int, pos_x: int, pos_y: int, 
                 font: pygame.font.Font, color: tuple, win_width: int,
                 win_height: int):
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
        self.name = name
        self.size = size
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.font = font
        self.color = color
        self.win_width = win_width
        self.win_height = win_height

    def drawing(self, screen):
        '''
        Renders title text and draws it centered horizontally on the screen.

        Args:
            screen (pygame.Surface): The surface where title will be blitted.

        Returns:
            None
        '''
        txt_title = self.font.render(self.name, True, self.color)
        pos_x = self.win_width // 2 - txt_title.get_width() // 2
        screen.blit(txt_title, (pos_x, self.pos_y))