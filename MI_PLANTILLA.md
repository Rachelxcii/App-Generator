# WELCOME TO DOCUMENTATION

You are just one step closer to your new app.

## 1. Coordinates & Units

It's fundamental to start clarifing:

- Origin is located in (0,0), and it's associated with leftish upper corner of the window.
- X axe: Grows to the right.
- Y axe: Grows downward.
- Position variable: (x, y) 
- Size varibale: (width, height)
- Units:
    - x, y, width, height are expressed in pixels (px).


## 2. Global parameters: Window section

### Configuración Global: `window`

| Parameter | Type | Mandatory | Default Value | Description |
| :--- | :---: | :---: | :---: | :--- |
| `ID` | `str` | No | | Unique ID to identity Window |
| `width` | `int` | **Sí** | | Ancho de la ventana en píxeles |
| `height` | `int` | **Sí** | | Alto de la ventana en píxeles |
| `fps` | `int` | No | 60 | Frames por segundo (velocidad de refresco) |
| `init_screen` | `str` | **Sí** | | ID de la pantalla que se cargará al iniciar |
| `await_all_tasks` | `str` | No | False |  |
| `colors` | `str` | **Sí** | |  |
| `fonts` | `str` | **Sí** | |  |

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
            "black_rgb": [0, 0, 0]
        },
        "fonts": {
             "Quicksand_font":{
                "file": "Quicksand/Quicksand-Regular.ttf",
                "size": 50
            }
        }
    }
```


## 3. Screens

``` JSON
"sample_screen": {
        "ID": "SAMPLE-SCREEN",
        "elements": {
            --- HERE YOU CAN INCLUDE ELEMENTS FOR THE SCREEN ---
        }
}
```


## 4. Elements

- [x] Button
- [ ] Checkbox
- [ ] Dropdown
- [ ] Image Output
- [x] Image
- [x] Loading Icon
- [ ] Slider
- [x] Text
- [x] Text Input
- [x] Text Output

### Button

Elemento interactivo que dispara funciones o redirecciones.
Obligatorios:
id: String único para vinculación de datos.
type: Debe ser "button".
subtype: 
position: Dict con x e y. Define la esquina superior izquierda.

If subtype is "text": 
text: String que se mostrará en el botón.
Opcionales:
functions: Lista de strings con nombres de funciones registradas.
redirection: ID de la pantalla a la que saltar tras el clic.
color: Nombre del color definido en la configuración global.

```json
"ejemplo_boton": {
    "type": "button",
    "position": {"x": 100, "y": 100},
    "text": "Click aquí"
}
``` 

### Image

### Loading Icon

### Text

### Text Input

### Text Output

Campo de texto dinámico vinculado a resultados de funciones.
Obligatorios:
id: String único para vinculación de datos.
output_functions: Lista de funciones a las que este elemento está suscrito (Hooks).
Opcionales:
initial_text: Texto que se muestra antes de recibir datos.
size: Dict con width y height. Si se define, el texto se escalará para encajar (usando smoothscale).


## 5. Inputs Logic

## 6. Hooks Logic
"Cuando una función listada en functions termina su ejecución en el Worker Thread, el sistema busca todos los elementos cuyo output_functions coincida con el nombre de dicha función y actualiza su contenido automáticamente."

## 7. Outputs Logic

## 8. Functions

### 8.1 Internal Functions (Pre-Defined)

### 8.2 External Functions




