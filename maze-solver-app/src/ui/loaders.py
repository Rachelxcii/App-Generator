import pygame
from pathlib import Path

from src.ui.elements import Title, Button


def buttons_loader(config: dict, colors: dict, fonts: dict) -> list:
    '''
    config = only buttons config
    '''
    buttons = []

    for line_cfg in config.values():

        buttons_name = line_cfg['names']
        alignment = line_cfg['alignment']
        width_button = line_cfg['size']['width']
        height_button = line_cfg['size']['height']
        dist_edge = line_cfg['dist_to_edge']
        space_buttons = line_cfg['dist_between_buttons']
        position = line_cfg['position']
        font = fonts[line_cfg['font']]
        color_base = colors[line_cfg['color']['base']]
        color_hover = colors[line_cfg['color']['hover']]

        
        for i, name in enumerate(buttons_name):

            x_pos, y_pos = position['x'], position['y']
            if alignment == "horizontal":  
                x_pos = dist_edge + (i * width_button) + (i * space_buttons)
            elif alignment == "vertical":
                y_pos = dist_edge + (i * height_button) + (i * space_buttons)

            buttons.append(Button(
                x_pos, y_pos, width_button, height_button, name, font, 
                color_base, color_hover
                ))
            
    return buttons


def fonts_loader(config: dict) -> dict:
    '''
    config = only fonts config
    '''
    # Locate root (from maze-solver-app/src/utils/ to maze-solver-app/)
    root_path = Path(__file__).resolve().parent.parent.parent
    fonts_path = root_path / 'assets' / 'fonts' 

    fonts = {}
    for key, data in config.items():
        path = fonts_path / data['file']
        fonts[key] = pygame.font.Font(str(path), data['size'])

    return fonts


def title_loader(config:dict, colors: dict, fonts: dict, window: dict) -> Title:
    '''
    config = only title config
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