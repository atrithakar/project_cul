from tabulate import tabulate
import os
import json
from colorful_outputs import print_in_yellow, print_in_red
from common_variables import C_CPP_MODULES_DLD_DIR

def freeze_2(invoked_by_list_modules=False):
    '''
    SAME AS freeze() FUNCTION, BUT IT'S USED WHEN THE PROJECT IS NOT INITIALIZED AND THE USER WANTS TO LIST THE MODULES
    '''
    if not os.path.isdir(C_CPP_MODULES_DLD_DIR):
        print_in_yellow("Warning: 'c_cpp_modules_dld' directory not found.")
        return

    if len(os.listdir(C_CPP_MODULES_DLD_DIR)) == 0:
        print_in_yellow("Warning: 'c_cpp_modules_dld' directory is empty.")
        return

    output = []

    # Loop through all the directories in 'c_cpp_modules_dld' directory and get the module name and version from 'module_info.json' file and append it to the output list. If invoked_by_list_modules is True, return the output list without processing else print the output list in a formatted way.
    for module in os.listdir(C_CPP_MODULES_DLD_DIR):
        module_path = os.path.join(C_CPP_MODULES_DLD_DIR, module)
        if os.path.isdir(module_path):
            versions_file = os.path.join(module_path, "module_info.json")
            if os.path.isfile(versions_file):
                try:
                    with open(versions_file, 'r') as vf:
                        versions_data = json.load(vf)
                        this_version = versions_data.get("version", "unknown")
                        output.append(f"{module}=={this_version}")
                except (json.JSONDecodeError, IOError) as e:
                    output.append(f"{module}==error({e})")
            else:
                output.append(f"{module}==no_version_file")
        else:
            output.append(f"{module}==not_a_directory")

    formatted_output = "\n".join(output)
    if invoked_by_list_modules:
        return output
    else:
        print(formatted_output)

def freeze(invoked_by_list_modules=False):
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
        freeze_2(invoked_by_list_modules) # so we call freeze_2() function to list the modules
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