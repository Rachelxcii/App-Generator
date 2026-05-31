import sys
from pathlib import Path

def get_base_path():
    '''
    Detects if the application is running from source code or as a 
    frozen executable (e.g., .exe or .app).
    '''
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    else:
        return Path(__file__).resolve().parent.parent.parent.parent
    

class AppPaths:
    """
    Manages the application's filesystem structure and asset resolution.
    """
    def __init__(self, root_name: str = "app-generator"):
        self.base_dir = get_base_path()
        self.assets_dir = self.base_dir / root_name / "assets"
        self.images = self.assets_dir / "images"
        self.fonts = self.assets_dir / "fonts"
        self.config = self.base_dir / root_name / "config"

    def to_dict(self) -> dict:
        """Returns a dictionary mapping for legacy compatibility."""
        return {
            'base': self.base_dir,
            'assets': self.assets_dir,
            'images': self.images,
            'fonts': self.fonts
        }
