import pygame

from src.utils.config_loader import get_config
from src.ui.loaders import fonts_loader
from src.ui.screen_renderer import screens_loader
from src.utils.path_loader import get_base_path


# Load configuration
config = get_config()

# Load path app #TO-DO improve the path logic
BASE_DIR = get_base_path()
ASSETS_DIR = BASE_DIR / "App-Generator" / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
FONTS_DIR = ASSETS_DIR / "fonts"

paths = {
    'BASE_DIR': get_base_path(),
    'ASSETS_DIR': ASSETS_DIR,
    'images_dir': IMAGES_DIR,
    'fonts_dir': FONTS_DIR,
}


# Initialize pygame font
if not pygame.font.get_init():
    pygame.font.init()

# Load ui configuration
display_cfg = config['display']
display_cfg['paths'] = paths
display_cfg['fonts'] = fonts_loader(display_cfg=config['display'])
screens_cfg = {k: v for k, v in config.items() if k.endswith("_screen")}

# --- NEW CODE ---
def run_app():

    # Initialize base display
    pygame.init()
    display = pygame.display.set_mode((display_cfg['width'], display_cfg['height']))
    current_state = display_cfg['init_screen']

    # Dictionary with states (screens)
    screens = screens_loader(display_cfg=display_cfg, screens_cfg=screens_cfg)

    clock = pygame.time.Clock()

    while current_state != 'exit':
        active_screen = screens[current_state]
        
        for event in pygame.event.get():
            # TO-DO: La pantalla decide qué estado sigue
            new_state = active_screen.handle_events(event)
            if new_state:
                print(f'FROM: {current_state} - TO: {new_state}')
                current_state = new_state

        active_screen.draw(display)
        pygame.display.flip()
        clock.tick(display_cfg['fps'])

    pygame.quit()


if __name__ == '__main__':
    if screens_cfg:
        run_app()
    else:
        print('WARNING: NO SCREENS DETECTED')



# TO-DO: en el config JSON en la parte de los botones crear para cada boton
# el parametro "action" que dice si es de tipo: goto, function.
# El tipo goto: redirecciona al user a otra pantalla.
# El tipo function: tiene una funcion especifica para el tipo de boton.

# TO-DO: en el config JSON crear "elementos generales" donde se guarden:
# config del return button, config del reset, config del save, config del exit

# TO-DO: revisar ocmo usar el arial en fonts, crear un param que se llame 
# "fuente personalizada" y que sea un bool.

# TO-DO: test que verifique que hay una fuente de titulo por cada screen, 
# con el nombre adecuado, ie: main_screen has title_main_screen, tambien en
# colors, con verificar que tienen colores asignados cada elemento vale, creo...

# TO-DO: se cargan para todo el colors y el fonts, hacerlo generico?