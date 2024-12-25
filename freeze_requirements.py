from tabulate import tabulate
import os
import json
from colorful_outputs import print_in_yellow
from common_variables import C_CPP_MODULES_DLD_DIR

def freeze_2(invoked_by_list_modules=False):
    if not os.path.isdir(C_CPP_MODULES_DLD_DIR):
        print_in_yellow("Warning: 'c_cpp_modules_dld' directory not found.")
        return

    if len(os.listdir(C_CPP_MODULES_DLD_DIR)) == 0:
        print_in_yellow("Warning: 'c_cpp_modules_dld' directory is empty.")
        return

    output = []

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
    try:
        with open("module_info.json", 'r') as f:
            versions = json.load(f)['requires']
            # versions = versions['requires']
        if invoked_by_list_modules:
            return versions
        print("\n".join(versions))
    except FileNotFoundError as e:
        freeze_2(invoked_by_list_modules)
    except Exception as e:
        print_in_red(f"Unexpected Error: {e}")

def list_modules():
    output = freeze(True)
    table_data = [module.split("==") for module in output]

    print(tabulate(table_data, headers=["Package", "Version"], tablefmt="simple"))