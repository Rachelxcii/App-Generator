# WELCOME TO DOCUMENTATION

You are just one step closer to your new app.

## 1. Coordinates & Units

It's fundamental to start clarifying:

- Origin is located in (0,0), and it's associated with the top-left corner of the window.
- X axis: Grows to the right.
- Y axis: Grows downward.
- Position variable: (x, y) 
- Size variable: (width, height)
- Units:
    - x, y, width, height are expressed in pixels (px).

## 2. Global parameters: Window section

### Configuración Global: `window`

| Parameter | Type | Mandatory | Default Value | Description |
| :--- | :---: | :---: | :---: | :--- |
| `ID` | `str` | No | "MAIN_WINDOW" | Unique ID to identify the Window instance. |
| `width` | `int` | **Yes** | | Width of the window in pixels. |
| `height` | `int` | **Yes** | | Height of the window in pixels. |
| `fps` | `int` | No | 60 | Frames per second (refresh rate) for the rendering loop. |
| `init_screen` | `str` | **Yes** | | ID of the initial screen to be loaded on startup. |
| `await_all_tasks` | `bool` | No | False | If true, the engine waits for all background threads to finish before closing. |
| `colors` | `dict` | **Yes** | | Dictionary mapping color names to RGB lists (e.g., [255, 255, 255]). |
| `fonts` | `dict` | **Yes** | | Dictionary of font configurations including file paths and sizes. |

### Example JSON: `window`

```JSON
"window": {
        "ID": "WINDOW",
        "width": 700,
        "height": 500,
        "fps": 60,
        "init_screen": "SAMPLE-SCREEN",
        "await_all_tasks": false,
        "colors": {
            "white_rgb": [255, 255, 255],
            "black_rgb": [0, 0, 0],
            "blue_ui": [0, 120, 215]
        },
        "fonts": {
             "Quicksand_font": {
                "file": "Quicksand/Quicksand-Regular.ttf",
                "size": 50
            },
            "Arial_small": {
                "file": "Arial.ttf",
                "size": 14
            }
        }
    }
```

## 3. Screens

Screens act as containers for UI elements. Only one screen is active and rendered at a time.

``` JSON
"sample_screen": {
        "ID": "SAMPLE-SCREEN",
        "elements": {
            "title_text": {
                "type": "text",
                "text": "Main Menu",
                "position": {"x": 50, "y": 50},
                "font": "Quicksand_font"
            },
            "start_btn": {
                "type": "button",
                "subtype": "text",
                "text": "Start Task",
                "position": {"x": 50, "y": 150},
                "functions": ["process_data_func"]
            }
        }
}
```

## 4. Elements

- [x] Button
- [x] Checkbox
- [x] Dropdown
- [x] Image Output
- [x] Image
- [x] Loading Icon
- [x] Slider
- [x] Text
- [x] Text Input
- [x] Text Output

### Button
Interactive element that triggers logic or screen changes.
**Mandatory:**
- `id`: Unique string.
- `type`: "button".
- `subtype`: "text" or "image".
- `position`: Dict with `x` and `y`.

**Subtype specific:**
- If "text": `text` (string) and `font` (ID) are required.
- If "image": `path` (string) is required.

**Optional:**
- `functions`: List of registered function names to execute on click.
- `redirection`: ID of the screen to load after click.
- `color`: Color name from global config.

### Image
Static visual component.
**Mandatory:**
- `type`: "image".
- `path`: Local path to the image file.
- `position`: Dict with `x` and `y`.
**Optional:**
- `size`: Dict with `width` and `height` for scaling.

### Loading Icon
Animated rotating element used during background tasks.
**Mandatory:**
- `type`: "loading_icon".
- `path`: Path to the icon image.
- `position`: Dict with `x` and `y`.
**Optional:**
- `rotation_speed`: Integer defining degrees of rotation per frame.

### Text
Static label for displaying information.
**Mandatory:**
- `type`: "text".
- `text`: The string content.
- `font`: Font ID defined in global parameters.
- `position`: Dict with `x` and `y`.
**Optional:**
- `color`: Color ID from global parameters.

### Text Input
Field for user data entry.
**Mandatory:**
- `id`: Unique ID for value retrieval.
- `type`: "text_input".
- `position`: Dict with `x` and `y`.
- `size`: Dict with `width` and `height`.
**Optional:**
- `placeholder`: Hint text shown when empty.
- `font`: Font ID for the input text.

### Text Output
Dynamic text field linked to function results (Hooks).
**Mandatory:**
- `id`: Unique ID.
- `type`: "text_output".
- `output_functions`: List of function names this element listens to.
**Optional:**
- `initial_text`: Placeholder text.
- `size`: Dict with `width` and `height` (triggers smoothscale if text exceeds bounds).

## 5. Inputs Logic
The system captures user interactions through the main event loop. 
- **Mouse Clicks:** Detected on elements with interactive types (`button`, `dropdown`, `checkbox`). The system checks if the mouse coordinates collide with the element's bounding box (derived from `position` and `size`).
- **Keyboard:** Active when a `text_input` element has focus. Characters are appended to the element's internal buffer and mirrored to the screen.

## 6. Hooks Logic
"When a function listed in `functions` finishes its execution in the Worker Thread, the system searches for all elements whose `output_functions` match the name of that function and updates their content automatically." This allows for asynchronous UI updates without freezing the main rendering thread.

## 7. Outputs Logic
The system maps the return values of functions executed in the Worker Thread to UI components. If a function returns a string or object, the `TextOutput` or `ImageOutput` components subscribed to that function ID will process the data (e.g., updating the text property or refreshing the image surface) and trigger a re-render of that specific component.

## 8. Functions

### 8.1 Internal Functions (Pre-Defined)
- `set_screen(screen_id)`: Changes the active screen to the provided ID.
- `exit_app()`: Safely closes the application window and terminates threads.
- `clear_inputs()`: Resets all `text_input` buffers on the current screen.

### 8.2 External Functions
These are Python functions defined in the logic layer of the codebase. They must be registered in the function mapping to be callable by the UI. External functions receive inputs from `text_input` elements automatically if their IDs are passed as arguments. They run in a `Worker Thread` to prevent UI blocking during heavy computations or I/O operations.
