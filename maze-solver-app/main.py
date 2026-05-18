import pygame

from src.utils.config_loader import get_config
from src.ui.loaders import fonts_loader
from src.ui.screen_renderer import screens_loader


# Load configuration
config = get_config()

# Initialize pygame font
if not pygame.font.get_init():
    pygame.font.init()

# Load ui configuration
window_cfg = config['window']
colors_cfg = config['colors']
fonts_cfg = fonts_loader(config=config['fonts'])
screens_cfg = {k: v for k, v in config.items() if k.endswith("_screen")}

# --- NEW CODE ---
def run_app():
    # Inicialización única
    pygame.init()
    screen = pygame.display.set_mode((window_cfg['width'], window_cfg['height']))
    
    # Diccionario de estados (Pantallas)
    screens = screens_loader(window=window_cfg, colors=colors_cfg, 
                           fonts=fonts_cfg, config=screens_cfg)
    
    current_state = 'MAIN-SCREEN'
    clock = pygame.time.Clock()

    while current_state != 'exit':
        active_screen = screens[current_state]
        
        for event in pygame.event.get():
            # TO-DO: La pantalla decide qué estado sigue
            new_state = active_screen.handle_events(event)
            if new_state:
                print(f'FROM: {current_state} - TO: {new_state}')
                current_state = new_state

        active_screen.draw(screen)
        pygame.display.flip()
        clock.tick(window_cfg['fps'])

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