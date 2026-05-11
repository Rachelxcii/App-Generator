from pathlib import Path
import pygame

def load_all_fonts(config_fonts: dict) -> dict:
    '''
    
    '''
    # Locate root (from maze-solver-app/src/utils/ to maze-solver-app/)
    root_path = Path(__file__).resolve().parent.parent.parent
    fonts_path = root_path / 'assets' / 'fonts' 

    fonts = {}
    for key, data in config_fonts.items():
        # Skip metadata or anotehr information
        if key.startswith("_"): 
            continue
        path = fonts_path / data['file']
        fonts[key] = pygame.font.Font(str(path), data['size'])

    return fonts


'''
root_path = Path(__file__).resolve().parent.parent.parent

# Small button config
sml_button_name = config['fonts']['sml_button']['file']
sml_button_size = config['fonts']['sml_button']['size']
sml_button_path = root_path / 'assets' / 'fonts' / sml_button_name
font_sml_button = pygame.font.Font(str(sml_button_path), sml_button_size)

# Medium button config
mid_button_name = config['fonts']['mid_button']['file']
mid_button_size = config['fonts']['mid_button']['size']
mid_button_path = root_path / 'assets' / 'fonts' / mid_button_name
font_mid_button = pygame.font.Font(str(mid_button_path), mid_button_size)

# Big button config
big_button_name = config['fonts']['big_button']['file']
big_button_size = config['fonts']['big_button']['size']
big_button_path = root_path / 'assets' / 'fonts' / big_button_name
font_big_button = pygame.font.Font(str(big_button_path), big_button_size)

# Main title config
main_title_name = config['fonts']['main_title']['file']
main_title_size = config['fonts']['main_title']['size']
main_title_path = root_path / 'assets' / 'fonts' / main_title_name
font_main_title = pygame.font.Font(str(main_title_path), main_title_size)
'''

if __name__ == '__main__':
    pass

'''
def get_font_button_32():
    return pygame.font.Font(str(supermercado_path), 32)

def get_font_title():
    return pygame.font.Font(str(supermercado_path), 72)
'''
