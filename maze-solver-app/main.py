# Starting script
from src.ui.renderer import main_screen
from src.utils.config_loader import get_config

# Load configuration
config = get_config()

if __name__ == "__main__":
    main_screen() 