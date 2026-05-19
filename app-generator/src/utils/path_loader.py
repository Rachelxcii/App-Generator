import sys
from pathlib import Path

def get_base_path():
    '''
    Detects if the application is running from source code or as a 
    frozen executable (e.g., .exe or .app).
    '''
    if getattr(sys, 'frozen', False):
        # When running as a bundled executable, PyInstaller extracts data 
        # to a temporary folder stored in sys._MEIPASS
        return Path(sys._MEIPASS)
    else:
        # When running from source, calculate the root directory by 
        # resolving the current file path and navigating up the parent tree
        return Path(__file__).resolve().parent.parent.parent.parent
