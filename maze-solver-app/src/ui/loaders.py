import pygame
from pathlib import Path

from src.ui.elements import Button


def fonts_loader(config_fonts: dict) -> dict:
    '''
    
    '''
    # Locate root (from maze-solver-app/src/utils/ to maze-solver-app/)
    root_path = Path(__file__).resolve().parent.parent.parent
    fonts_path = root_path / 'assets' / 'fonts' 

    fonts = {}
    for key, data in config_fonts.items():
        path = fonts_path / data['file']
        fonts[key] = pygame.font.Font(str(path), data['size'])

    return fonts

def buttons_loader(config: dict, colors: dict, fonts: dict) -> list:
    '''
    
    '''
    buttons = []

    for line_config in config['buttons'].values():

        buttons_name = line_config['names']
        alignment = line_config['alignment']
        width_button = line_config['size']['width']
        height_button = line_config['size']['height']
        dist_edge = line_config['dist_to_edge']
        space_buttons = line_config['dist_between_buttons']
        position = line_config['position']
        
        for i, name in enumerate(buttons_name):

            x_pos, y_pos = position['x'], position['y']
            if alignment == "horizontal":  
                x_pos = dist_edge + (i * width_button) + (i * space_buttons)
            elif alignment == "vertical":
                y_pos = dist_edge + (i * height_button) + (i * space_buttons)

            buttons.append(Button(
                x_pos, y_pos, width_button, height_button, name, 
                fonts['sml_button'], colors['button_base'], 
                colors['button_hover']
                ))
            
    return buttons


if __name__ == '__main__':
    pass