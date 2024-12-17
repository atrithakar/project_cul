import os
import sys
import shutil
import json
import os
from colorama import Fore, init
from tabulate import tabulate
import zipfile
import urllib.request
import io

init(autoreset=True)

def print_in_red(message):
    print(Fore.RED + message)

def print_in_yellow(text):
    print(Fore.YELLOW + text)

def print_in_green(text):
    print(Fore.GREEN + text)


C_CPP_MODULES_DLD_DIR = "./c_cpp_modules_dld"
BASE_URL = "https://culb.vercel.app"
# BASE_URL = "http://192.168.0.104:5000"

def check_requirements_and_download(module_name, version=''):
    try:
        version_url = f"{BASE_URL}/versions/{module_name}"
        with urllib.request.urlopen(version_url) as response:
            if response.status != 200:
                raise Exception(f"HTTP {response.status}: Unable to fetch versions.")
            
            version_data = response.read().decode()
            version_info = json.loads(version_data)
        
        requirements = version_info.get("requires", {})
        latest_version = version_info.get("latest", "unknown")
        target_version = version or latest_version
        modules_to_install = requirements.get(target_version)
        
        if not modules_to_install:
            return None
        
        print_in_green(f"Installing requirements for {module_name}")
        for module in modules_to_install:
            fetch_module(module.split("==")[0], module.split("==")[1])
    
    except urllib.error.HTTPError as http_err:
        print_in_red(f"HTTP error: {http_err.code} {http_err.reason}")
    except urllib.error.URLError as url_err:
        print_in_red(f"URL error: {url_err.reason}")
    except json.JSONDecodeError:
        print_in_red("Failed to decode JSON response. Please check the server response.")
    except KeyError as key_err:
        print_in_red(f"Key error: {key_err}")
    except Exception as e:
        print_in_red(f"Unexpected error: {e}")




def fetch_module(module_name, version=''):
    try:
        zip_url = f"{BASE_URL}/files/{module_name}/{version}"
        
        req = urllib.request.Request(zip_url)
        try:
            with urllib.request.urlopen(req) as response:
                if response.status != 200:
                    raise Exception(f"HTTP {response.status}: Unable to fetch module.")
                
                zip_data = response.read()
            
            zip_stream = io.BytesIO(zip_data)
            
            module_dir = os.path.join(C_CPP_MODULES_DLD_DIR, module_name)
            os.makedirs(module_dir, exist_ok=True)
            
            with zipfile.ZipFile(zip_stream, 'r') as zip_ref:
                zip_ref.extractall(module_dir)
                print_in_green(f"Module '{module_name}' is successfully installed.")
            check_requirements_and_download(module_name, version)
        except urllib.error.HTTPError as e:
            error_message = e.read().decode()
            error_message = json.loads(error_message)
            print_in_red(f"Error: {error_message.get('error')}")
        except urllib.error.URLError as e:
            print_in_red(f"Error: Unable to connect to the server. Reason: {e.reason}")
    except Exception as e:
        print_in_red(f"Unexpected error: {e}")

def install(library):
    if "==" in library:
        fetch_module(library.split("==")[0], library.split("==")[1])
    else:
        fetch_module(library)

def uninstall(library):
    library_path = os.path.join(C_CPP_MODULES_DLD_DIR, library)
    if os.path.isdir(library_path):
        try:
            shutil.rmtree(library_path)
            print_in_green(f"Successfully uninstalled {library}.")
        except Exception as e:
            print_in_red(f"Error uninstalling library: {e}")
    else:
        print_in_yellow(f"Warning: Library '{library}' not found in 'c_cpp_modules_dld'.")

def update(library):
    if(os.path.isdir(os.path.join(C_CPP_MODULES_DLD_DIR, library))):
        print(f"Updating {library}...")
        install(library)
    else:
        print_in_yellow(f"Warning: Library '{library}' not found in 'c_cpp_modules_dld'.")

def help_message():
    help_text = """
    cul CLI - Command Line Interface for managing C/C++ libraries
    
    Commands:
        install <library>    - Installs the specified C/C++ library.
        uninstall <library>  - Uninstalls the specified library.
        update <library>     - Updates the specified library to the latest version.
        list                 - Lists all installed libraries.
        freeze               - Outputs the installed libraries in requirements.txt format.
        help                 - Shows this help message.

    """
    print(help_text)

def freeze(invoked_by_list_modules=False):
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

def list_modules():
    output = freeze(True)
    table_data = [module.split("==") for module in output]

    print(tabulate(table_data, headers=["Package", "Version"], tablefmt="simple"))

def main():
    
    if len(sys.argv) < 2:
        help_message()
        return

    command = sys.argv[1]

    if command == 'install':
        if len(sys.argv) < 3:
            print_in_red("Error: No library specified for installation.")
            help_message()
        else:
            install(sys.argv[2])
    elif command == 'uninstall':
        if len(sys.argv) < 3:
            print_in_red("Error: No library specified for uninstallation.")
            help_message()
        else:
            uninstall(sys.argv[2])
    elif command == 'update':
        if len(sys.argv) < 3:
            print_in_red("Error: No library specified for updating.")
            help_message()
        else:
            update(sys.argv[2])
    elif command == 'help':
        help_message()
    elif command == 'freeze':
        freeze()
    elif command == 'list':
        list_modules()
    elif command == 'check':
        if len(sys.argv) < 3:
            print_in_red("Error: No library specified for checking.")
            help_message()
        else:
            check_requirements(sys.argv[2])
    else:
        print_in_red(f"Unknown command: {command}")
        help_message()

if __name__ == "__main__":
    main()
