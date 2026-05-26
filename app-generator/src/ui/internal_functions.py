import pygame

'''
app_functions_registry = {
    "reset": src.ui.app_functions.reset_maze,
    "save": src.ui.app_functions.save_data,
    "exit": src.ui.app_functions.custom_exit
}
        '''

def exit(screen_instance):
    return "exit"

def reset_maze(screen_instance):
    """
    Resets the maze generation state.
    Accesses the screen instance to trigger a new generation sequence.
    """
    print("System: Resetting maze environment...")
    # TO-DO: screen_instance.maze.generate()

    
def save_data(screen_instance):
    """
    Exports current session metrics or maze configurations to a persistent file.
    """
    print("System: Exporting session statistics to CSV...")
    # TO-DO: Logic for data persistence goes here



