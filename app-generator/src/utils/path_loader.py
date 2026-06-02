import sys
from pathlib import Path


def get_base_path():
    '''
    Determines the root directory of the application at runtime.

    This function handles the path resolution differently depending on the 
    execution context:
    1. Frozen: If the app is bundled (e.g., via PyInstaller), it retrieves the 
       temporary extraction path (sys._MEIPASS).
    2. Development: If running from source, it calculates the path relative to 
       this script's location.

    Returns:
        Path: The resolved base directory path.
    '''
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    else:
        return Path(__file__).resolve().parent.parent.parent.parent
    

class AppPaths:
    '''
    Centralizes filesystem orchestration and asset path resolution.

    This class provides a structured way to access images, fonts, and 
    configuration files across the entire framework, ensuring consistency 
    across different operating systems using Pathlib.

    Attributes:
        base_dir (Path): The root directory of the project.
        assets_dir (Path): Directory containing all static resources.
        images (Path): Path to the image and icon repository.
        fonts (Path): Path to the TrueType/OpenType font files.
        config (Path): Path to the JSON-based UI schemas.
    '''

    def __init__(self, root_name: str = 'app-generator'):
        '''
        Initializes the path tree based on the detected base directory.

        Args:
            root_name (str): The name of the main application package folder.
        '''
        self.base_dir = get_base_path()
        self.assets_dir = self.base_dir / root_name / 'assets'
        self.images = self.assets_dir / 'images'
        self.fonts = self.assets_dir / 'fonts'
        self.config = self.base_dir / root_name / 'config'


    def to_dict(self) -> dict:
        '''
        Serializes the path objects into a dictionary.

        Mainly used for legacy compatibility with components that expect 
        dictionary-based configuration lookups.

        Returns:
            dict: A mapping of directory identifiers to Path objects.
        '''
        return {
            'base': self.base_dir,
            'assets': self.assets_dir,
            'images': self.images,
            'fonts': self.fonts
        }
