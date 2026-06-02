import pygame

from src.ui.elements.image import Image


def loading_icons_loader(display_cfg: dict, loading_icons_cfg: dict) -> list:
    '''
    Parses configuration data to instantiate UI Loading Icon objects.

    Args:
        display_cfg (dict): Global display and asset settings.
        text_inputs (dict): Nested dictionary containing loading icons
                            configuration.

    Returns:
        list: A collection of initialized TextInput instances.
    '''
    loading_icons = []
    for loading_icon_cfg in loading_icons_cfg:
        loading_icons.append(LoadingIcon(display_cfg=display_cfg,
                                         loading_icon_cfg=loading_icon_cfg))
    return loading_icons


class LoadingIcon:
    '''
    A reactive UI component that visualizes background process activity.

    This class acts as a "monitor" for specific functions running in the Worker 
    Thread. It remains invisible or static until the monitored function is 
    active, at which point it triggers its internal animation 
    (typically rotation).

    Attributes:
        id (str): Unique identifier for the icon.
        display_cfg (dict): Global configuration for paths and colors.
        loading_icon_cfg (dict): Specific configuration.
        func (str): The name of the registered function this icon is tracking.
        is_running (bool): State flag synced with the "func" execution status.
        image (Image): The underlying Image instance handling the pixels.
    '''

    def __init__(self, display_cfg: dict, loading_icon_cfg: dict):
        '''
        Initializes the LoadingIcon and links it to a monitored process.

        Args:
            display_cfg (dict): Global configuration dictionary.
            loading_icon_cfg (dict): Component-specific settings from JSON.
        '''
        self.id = loading_icon_cfg['id']

        self.func = loading_icon_cfg['monitored_function']
        self.is_running = False

        self._load_image(display_cfg=display_cfg,
                         loading_icon_cfg=loading_icon_cfg)


    def _load_image(self, display_cfg: dict, loading_icon_cfg: dict) -> None:
        '''
        Composition step: Creates an Image instance to handle rendering logic.
        '''
        self.image =  Image(display_cfg=display_cfg, 
                            image_cfg=loading_icon_cfg)


    def draw(self, screen: pygame.Surface) -> None:
        '''
        Renders the loading animation if the monitored function is currently 
        executing.
        
        The actual rotation logic is encapsulated within the self.image.draw() 
        method, assuming the 'rotation' flag was set in the JSON configuration.

        Args:
            screen (pygame.Surface): The target surface for rendering.
        '''
        if self.is_running:
            self.image.draw(screen)
