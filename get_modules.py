import inspect
import simple_bot as module

def all_commands():
    functions = []
    for function in inspect.getmembers(module, inspect.isfunction):
        functions.append(f'/{function[0]}')
    return functions

get_functions()

