from tabulate import tabulate
import os
import json
from colorful_outputs import print_in_yellow, print_in_red
from common_variables import C_CPP_MODULES_DLD_DIR
from helper_functions import parse_module

def freeze_not_initialized(invoked_by_list_modules: bool = False):
    '''
    Prints the list of modules along with their versions if the project is not initialized

    Args:
        invoked_by_list_modules (bool): If True, the function was invoked by list_modules() function

    Returns:
        versions: List of modules along with their versions, if invoked_by_list_modules is True
        None: If invoked_by_list_modules is False

    Raises:
        json.JSONDecodeError: If the JSON decoding fails
        IOError: If there is an I/O error
        Exception: If any unexpected error occurs

    '''
    if not os.path.isdir(C_CPP_MODULES_DLD_DIR):
        print_in_yellow("Warning: 'c_cpp_modules_dld' directory not found.")
        return

    if not os.listdir(C_CPP_MODULES_DLD_DIR):
        print_in_yellow("Warning: 'c_cpp_modules_dld' directory is empty.")
        return

    output = []
    
    for module in os.listdir(C_CPP_MODULES_DLD_DIR):
        module_path = os.path.join(C_CPP_MODULES_DLD_DIR, module)
        if not os.path.isdir(module_path):
            output.append(f"{module}==not_a_directory")
            continue

        versions_file = os.path.join(module_path, "module_info.json")
        if not os.path.isfile(versions_file):
            output.append(f"{module}==no_version_file")
            continue

        try:
            with open(versions_file, 'r') as vf:
                versions_data = json.load(vf)
                this_version = versions_data.get("version", "unknown")
                output.append(f"{module}=={this_version}")

        except json.JSONDecodeError:
            output.append(f"{module}==error(JSONDecodeError: Invalid JSON format)")
        except IOError as e:
            output.append(f"{module}==error(IOError: {e})")
        except Exception as e:
            output.append(f"{module}==error(Unexpected: {e})")

    formatted_output = "\n".join(output)
    if invoked_by_list_modules:
        return output
    print(formatted_output)


def freeze(invoked_by_list_modules: bool = False):
    '''
    Prints the list of modules along with their versions

    Args:
        invoked_by_list_modules (bool): If True, the function was invoked by list_modules() function

    Returns:
        versions: List of modules along with their versions, if invoked_by_list_modules is True

    Raises:
        Unexpected Error: If any unexpected error occurs
    '''
    try:
        with open("module_info.json", 'r') as f:
            versions = json.load(f)['requires']
        if invoked_by_list_modules: 
            return versions
        print("\n".join(versions))
    except FileNotFoundError as e:
        return freeze_not_initialized(invoked_by_list_modules)
    except Exception as e:
        print_in_red(f"Unexpected Error: {e}")

def list_modules():
    '''
    Lists the modules along with their versions

    Args:
        None

    Returns:
        None

    Raises:
        None
    '''
    output = freeze(True) # call freeze() function with True to get the list of modules along with their versions without formatting
    table_data = [parse_module(module) for module in output]
    print(tabulate(table_data, headers=["Package", "Version"], tablefmt="simple"))