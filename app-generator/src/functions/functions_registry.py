import src.functions.internal_functions
import src.functions.external_functions


internal_functions_registry = {
    'sleep_timer': src.functions.internal_functions.sleep_timer,
    'read_prompt': src.functions.internal_functions.read_prompt
}

external_functions_registry = {
    'reset': src.functions.external_functions.reset_maze,
    'save': src.functions.external_functions.save_data
}