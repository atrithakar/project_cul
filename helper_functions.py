'''
This file contains the helper functions used in the project.
The purpose of this file is to make it easier to manage the functions that are used in multiple files.
These functions are the ones which are tiny and are used in multiple files.
'''

def ensure_dir_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def parse_module(module_name_str):
    return module_name_str.split("==") if "==" in module_name_str else [module_name_str, ""]

def check_if_dir_exists(directory):
    return os.path.exists(directory)