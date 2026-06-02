import time

# --- REMEMBER: ADD ALL FUNCTIONS IN FUNCTION REGISTRY ---

def sleep_timer(screen_instance, inputs):
    print('TIMER ACTIVATED')
    time.sleep(3)
    print('HAN PASADO 3 SECS')
    return 'TIMER OUTPUT'


def read_prompt(screen_instance, inputs):
    print(f'READING: {inputs}')
    return inputs['user_input_prompt']





