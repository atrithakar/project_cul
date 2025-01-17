from tabulate import tabulate
import os
import json
from colorful_outputs import print_in_yellow, print_in_red
from common_variables import C_CPP_MODULES_DLD_DIR

def freeze_2(invoked_by_list_modules: bool = False):
    '''
    SAME AS freeze() FUNCTION, BUT IT'S USED WHEN THE PROJECT IS NOT INITIALIZED AND THE USER WANTS TO LIST THE MODULES
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
        with open("module_info.json", 'r') as f: # open the module_info.json file in read mode
            versions = json.load(f)['requires'] # load the json data from the file and get the 'requires' key
            # versions = versions['requires']
        if invoked_by_list_modules: 
            return versions # return the list without processing if the function was invoked by list_modules()
        print("\n".join(versions)) # else print the module names along with their versions
    except FileNotFoundError as e: # file not found error will come if the project is not initialized, but we still want to list the modules
        return freeze_2(invoked_by_list_modules) # so we call freeze_2() function to list the modules
    except Exception as e:
        print_in_red(f"Unexpected Error: {e}") # print unexpected error if any

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
    output = freeze(True) # call freeze() function with True to get the list of modules along with their versions
    table_data = [module.split("==") for module in output] # split the module name and version
    print(tabulate(table_data, headers=["Package", "Version"], tablefmt="simple")) # tabulate the data and print it