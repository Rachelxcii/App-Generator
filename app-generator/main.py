import pygame

from src.utils.config_loader import get_config
from src.ui.loaders import fonts_loader
from src.ui.screen_renderer import screens_loader
from src.utils.path_loader import AppPaths


# --- TO-DO LIST ---
# TO-DO: pre-sets functions like: save CSV, reset, exit, etc. (internal_functions.py)
# TO-DO: move "app_functions_registry" from screen_renderer.py to internal_functions.py ('in')
# TO-DO: move "app_functions_registry" from screen_renderer.py to external_functions.py ('ex')
# TO-DO: unify "app_functions_registry" from 'in' and 'ex' in screen_renderer.py
# TO-DO: tests to check the entire config JSON


# --- Global Initialization and Asset Mapping ---
# Load global application settings from JSON
config = get_config()

# Load path registry for internal reference
paths = AppPaths().to_dict()

# Ensure the Pygame font module is ready for asset loading
if not pygame.font.get_init():
    pygame.font.init()

# Load ui configuration
display_cfg = config['display']
display_cfg['paths'] = paths
display_cfg['fonts'] = fonts_loader(display_cfg=config['display'])
screens_cfg = {k: v for k, v in config.items() if k.endswith("_screen")}


def run_app():
    '''
    Main execution loop. Initializes the display and manages state transitions 
    between different application screens.

    Logic:
        1. Initializes the Pygame display surface and clock.
        2. Loads all screen objects based on the configuration.
        3. Enters the main loop: 
           - Handles events through the active screen.
           - Updates current_state if a transition (redirection) is triggered.
           - Renders the active screen at the defined FPS.
    '''

    # Initialize base display
    pygame.init()
    display = pygame.display.set_mode((display_cfg['width'], 
                                       display_cfg['height']))

    # Set the starting point for the state machine
    current_state = display_cfg['init_screen']

    # Dictionary containing instantiated screen objects mapped by their ID
    screens = screens_loader(display_cfg=display_cfg, screens_cfg=screens_cfg)

    # Frame rate controller
    clock = pygame.time.Clock()

    # --- MAIN APPLICATION LOOP ---
    while current_state != 'exit':

        active_screen = screens[current_state]
        
        for event in pygame.event.get():
            new_state = active_screen.handle_events(event)
            if new_state:
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