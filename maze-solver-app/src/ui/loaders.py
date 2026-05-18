import pygame
from pathlib import Path

from src.ui.elements import Title, Button


def buttons_loader(config: dict, colors: dict, fonts: dict) -> list:
    '''
    Parses button configuration data to instantiate UI Button objects.
    
    This function handles the geometric distribution of buttons based on 
    alignment settings (horizontal or vertical) and grouped in blocks.
    And applies styling from global color and font dictionaries.

    Args:
        config (dict): Nested dictionary containing button configuration.
        colors (dict): Global RGB color palette mapping.
        fonts (dict): Pre-loaded pygame.font.Font objects.

    Returns:
        list: A collection of initialized Button instances.
    '''

    buttons = []

    for block_cfg in config.values():

        buttons_name = block_cfg['buttons']
        alignment = block_cfg['alignment']
        width_button = block_cfg['size']['width']
        height_button = block_cfg['size']['height']
        dist_edge = block_cfg['dist_to_edge']
        space_buttons = block_cfg['dist_between_buttons']
        position = block_cfg['position']
        font = fonts[block_cfg['font']]
        color_base = colors[block_cfg['color']['base']]
        color_hover = colors[block_cfg['color']['hover']]

        
        for i, name in enumerate(buttons_name):

            x_pos, y_pos = position['x'], position['y']
            if alignment == "horizontal":  
                x_pos = dist_edge + (i * width_button) + (i * space_buttons)
            elif alignment == "vertical":
                y_pos = dist_edge + (i * height_button) + (i * space_buttons)
            
            action_data = buttons_name[name]

            buttons.append(Button(
                x=x_pos, y=y_pos, weight=width_button, height=height_button, 
                text=name, font=font, color_base=color_base, 
                color_hover=color_hover, action_data=action_data
                ))
            
    return buttons


def fonts_loader(config: dict) -> dict:
    '''
    Resolves filesystem paths and initializes Pygame font assets.

    Uses pathlib for robust cross-platform path resolution, moving from the 
    current script location to the project root's asset directory.

    Args:
        config (dict): Mapping of font keys to file names and point sizes.

    Returns:
        dict: A dictionary where keys match config and values are 
        pygame.font.Font objects.
    '''

    # Locate root (from maze-solver-app/src/utils/ to maze-solver-app/)
    root_path = Path(__file__).resolve().parent.parent.parent
    fonts_path = root_path / 'assets' / 'fonts' 

    fonts = {}
    for key, data in config.items():
        path = fonts_path / data['file']
        # Convert Path object to string for Pygame compatibility
        fonts[key] = pygame.font.Font(str(path), data['size'])

    return fonts


def title_loader(config:dict, colors: dict, fonts: dict, 
                 window: dict) -> Title:
    '''
    Initializes the Title UI component with window context for centering logic.

    Args:
        config (dict): Current screen title configuration.
        colors (dict): Global RGB color palette mapping.
        fonts (dict): Pre-loaded pygame.font.Font objects.
        window (dict): Window dimensions for horizontal alignment calculations.

    Returns:
        Title: An instance of the Title class ready for rendering.
    '''

    title_name = config['name']
    title_size = config['size']
    title_pos_x = config['position']['x']
    title_pos_y = config['position']['y']
    title_font = fonts[config['font']]
    title_color = colors[config['color']]
    win_width = window['width']
    win_height = window['height']

    return Title(name=title_name, size=title_size, pos_x=title_pos_x, 
                 pos_y=title_pos_y, font=title_font, color=title_color,
                 win_width=win_width, win_height=win_height)


if __name__ == '__main__':
    pass