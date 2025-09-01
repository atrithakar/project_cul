import os
import shutil
from colorful_outputs import print_in_green, print_in_red, print_in_yellow
from helper_functions import parse_module
from common_variables import C_CPP_MODULES_DLD_DIR
from init import remove_requirements

def uninstall(module_name: str):
    '''
    Uninstalls the module from the 'c_cpp_modules_dld' directory

    Args:
        module_name (str): The name of the module to uninstall

    Returns:
        None

    Raises:
        Exception: If there is an error while uninstalling the module
    '''
    version_exists = False
    if("==" in module_name):
        module_name, _ = parse_module(module_name)
        
    module_path = os.path.join(C_CPP_MODULES_DLD_DIR, module_name)

    if not os.path.isdir(module_path):
        print_in_yellow(f"Warning: Module '{module_name}' not found in 'c_cpp_modules_dld'.")
        return

    try:
        shutil.rmtree(module_path)
        print_in_green(f"Successfully uninstalled {module_name}.")
        remove_requirements(module_name)
    except Exception as e:
        print_in_red(f"Error uninstalling module: {e}")