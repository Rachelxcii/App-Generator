import json
from pathlib import Path


def get_config() -> dict:
    """
    Reads the config.json file and returns its content as a dictionary.
    Ensures absolute path resolution to avoid FileNotFoundError.

    Returns:
        dict: Application settings.
    """

    # Locate aspp root (from maze-solver-app/src/utils/ to maze-solver-app/)
    root_path = Path(__file__).resolve().parent.parent.parent
    config_path = root_path / "config.json"

    try:
        with open(config_path, "r", encoding="utf-8") as file:
            raw_config = json.load(file)
            # Dictionary comprehension to skip keys starting with "_"
            # This cleans the top-level of your JSON automatically
            config = {k: v for k, v in raw_config.items() if not k.startswith("_")}
            return config
        
    except FileNotFoundError:
        print(f"Warning: {config_path} not found. Using default settings.")
        return {
                    "window": {
                        "width": 800,
                        "height": 600,
                        "title": "Maze Generator & Solver",
                        "fps": 60
                    },
                    "colors": {
                        "background": [30, 30, 30],
                        "button_base": [50, 50, 50],
                        "button_hover": [100, 100, 100],
                        "text_white": [255, 255, 255]
                    },
                    "fonts": {
                        "button": {
                            "file": "Arial",
                            "size": 32
                        }
                    }
                }
    
    
if __name__ == "__main__":
    print(get_config())