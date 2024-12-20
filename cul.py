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
import appdirs

init(autoreset=True)

def print_in_red(message):
    print(Fore.RED + message)

def print_in_yellow(text):
    print(Fore.YELLOW + text)

def print_in_green(text):
    print(Fore.GREEN + text)

CACHE_DIR = appdirs.user_cache_dir("CUL", "CUL_CLI")
C_CPP_MODULES_DLD_DIR = "./c_cpp_modules_dld"
BASE_URL = "https://culb.vercel.app"
# BASE_URL = "http://192.168.0.104:5000"

def cache_module(zip_ref, module_name, version='1.0.0'):
    try:
        os.makedirs(CACHE_DIR, exist_ok=True)
        cache_filepath = os.path.join(CACHE_DIR, f"{module_name}_v{version}")
        zip_ref.extractall(cache_filepath)
        print_in_green(f"Module '{module_name} version {version}' has been successfully cached.")
    except Exception as e:
        print_in_red(f"Error caching module: {e}")

def check_cache_and_install(module_name, version='1.0.0'):
    cache_filepath = os.path.join(CACHE_DIR, f"{module_name}_v{version}")
    if os.path.isdir(os.path.join(C_CPP_MODULES_DLD_DIR, module_name)):
        shutil.rmtree(os.path.join(C_CPP_MODULES_DLD_DIR, module_name))
    if os.path.isdir(cache_filepath):
        shutil.copytree(cache_filepath, os.path.join(C_CPP_MODULES_DLD_DIR, module_name))
        return True
    return False
    

def check_requirements_and_download(module_name, version='1.0.0'):
    try:
        # version_url = f"{BASE_URL}/versions/{module_name}"
        # with urllib.request.urlopen(version_url) as response:
        #     if response.status != 200:
        #         raise Exception(f"HTTP {response.status}: Unable to fetch versions.")
            
        #     version_data = response.read().decode()
        #     version_info = json.loads(version_data)

        version_json_path = os.path.join(C_CPP_MODULES_DLD_DIR, module_name, 'module_info.json')
        version_info = None
        with open(version_json_path, 'r') as f:
            version_info = json.load(f)
        # version_info = json.loads(version_json_path)
        # print(version_info)
        
        requirements = version_info.get("requires", {})
        # latest_version = version_info.get("latest", "unknown")
        # target_version = version or latest_version
        # modules_to_install = requirements.get(target_version)
        
        if not requirements:
            return None
        
        print_in_green(f"Installing requirements for {module_name}")
        for module in requirements:
            if check_cache_and_install(module.split("==")[0], module.split("==")[1]):
                print_in_green(f"Module '{module}' has been successfully installed from cache.")
                continue
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
    cached_module_version = None
    if version=='':
        cached_module_version = '1.0.0'
    if check_cache_and_install(module_name, cached_module_version or version):
        print_in_green(f"Module '{module_name}' Version '{cached_module_version or version}' has been successfully installed from cache.")
        check_requirements_and_download(module_name, version)
        return
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
                cache_module(zip_ref, module_name, cached_module_version or version)
                zip_ref.extractall(module_dir)
                print_in_green(f"Module '{module_name}' Version '{version}' has been successfully installed.")
            check_requirements_and_download(module_name, version)
        except urllib.error.HTTPError as e:
            error_message = e.read().decode()
            error_message = json.loads(error_message)
            print_in_red(f"Error: {error_message.get('error')}")
        except urllib.error.URLError as e:
            print_in_red(f"Error: Unable to connect to the server. Reason: {e.reason}")
    except Exception as e:
        print_in_red(f"Unexpected error: {e}")

def check_already_installed(module_name, version='1.0.0'):
    module_exists = os.path.isdir(os.path.join(C_CPP_MODULES_DLD_DIR, module_name))
    version_exists = False
    if module_exists:
        try:
            with open(os.path.join(C_CPP_MODULES_DLD_DIR, module_name, "module_info.json"), 'r') as f:
                module_info = json.load(f)
                if module_info.get("version") == version:
                    version_exists = True
        except (json.JSONDecodeError, IOError):
            # print(json.JSONDecodeError)
            # print(IOError)
            return False
        if module_exists and version_exists:
            return True
    
    else:
        return False

def install(module_name):
    # print(module_name)
    if "==" in module_name:
        module_name_ = module_name.split("==")[0]
        version = module_name.split("==")[1]
        if check_already_installed(module_name_, version):
            print_in_yellow(f"Module '{module_name_}' Version '{version}' is already installed.")
            return

        print(f"Installing {module_name_} Version {version}...")
        fetch_module(module_name_, version)
    else:
        if check_already_installed(module_name):
            print_in_yellow(f"Module '{module_name}' is already installed.")
            return

        fetch_module(module_name)

def uninstall(module_name):
    module_path = os.path.join(C_CPP_MODULES_DLD_DIR, module_name)
    if os.path.isdir(module_path):
        try:
            shutil.rmtree(module_path)
            print_in_green(f"Successfully uninstalled {module_name}.")
        except Exception as e:
            print_in_red(f"Error uninstalling module: {e}")
    else:
        print_in_yellow(f"Warning: Module '{module_name}' not found in 'c_cpp_modules_dld'.")

def update(module_name):
    if(os.path.isdir(os.path.join(C_CPP_MODULES_DLD_DIR, module_name))):
        print(f"Updating {module_name}...")
        fetch_module(module_name)
    else:
        print_in_yellow(f"Warning: Library '{module_name}' not found in 'c_cpp_modules_dld'.")

def help_message():
    help_text = """
    cul CLI - Command Line Interface for managing C/C++ libraries
    
    Commands:
        install library                            - Installs the specified C/C++ library.
        install library==version                   - Installs the specified version of the library.
        install library1 library2 library3 ...     - Installs multiple libraries. (Version is optional and can be specified for each library)
        uninstall library                          - Uninstalls the specified library.
        uninstall library1, library2, library3 ... - Uninstalls multiple libraries.
        update library                             - Updates the specified library to the latest version.
        update library1, library2, library3 ...    - Updates multiple libraries to the latest version.
        search library                             - Searches for the specified library and displays available versions.
        list                                       - Lists all installed libraries.
        freeze                                     - Outputs the installed libraries in requirements.txt format.
        help                                       - Shows the help message.

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

def search_module(module_name):
    try:
        search_url = f"{BASE_URL}/versions/{module_name}"

        with urllib.request.urlopen(search_url) as response:
            if response.status != 200:
                raise urllib.error.HTTPError(search_url, response.status, f"Unable to fetch versions for {module_name}.", response.getheaders(), None)
            
            module_data = response.read().decode()
            module_info = json.loads(module_data)
            print("Module name: ", module_name)
            available_versions = module_info.get("versions", [])
            latest_version = module_info.get("latest", "unknown")
            if available_versions:
                print("Available versions:")
                for version in available_versions:
                    print(f"  - {version.get('version')}")
                print(f"Latest version: {latest_version}")
            else:
                print_in_yellow("No versions available.")
            


    except urllib.error.HTTPError as http_err:
        # Detailed HTTP error message including the status code and reason
        print_in_red(f"HTTP error: {http_err.code} {http_err.reason}")
    
    except urllib.error.URLError as url_err:
        # Error handling for general URL errors (e.g., network issues, invalid URL)
        print_in_red(f"URL error: {url_err.reason}")
    
    except json.JSONDecodeError:
        # Error handling if JSON decoding fails
        print_in_red("Failed to decode the JSON response. Please check the server response.")
    
    except KeyError as key_err:
        # Error handling for missing keys in the JSON response
        print_in_red(f"Key error: {key_err}")
    
    except Exception as e:
        # General exception handling for unexpected errors
        print_in_red(f"Unexpected error: {e}")


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
            for i in range(2, len(sys.argv)):
                # print(sys.argv[i])
                # print("Installing...")
                install(sys.argv[i])
    elif command == 'uninstall':
        if len(sys.argv) < 3:
            print_in_red("Error: No library specified for uninstallation.")
            help_message()
        else:
            for i in range(2, len(sys.argv)):
                uninstall(sys.argv[i])
    elif command == 'update':
        if len(sys.argv) < 3:
            print_in_red("Error: No library specified for updating.")
            help_message()
        else:
            for i in range(2, len(sys.argv)):
                update(sys.argv[i])
    elif command == 'help':
        help_message()
    elif command == 'freeze':
        freeze()
    elif command == 'list':
        list_modules()
    elif command == 'search':
        if len(sys.argv) < 3:
            print_in_red("Error: No library specified for searching.")
            help_message()
        else:
            search_module(sys.argv[2])
    else:
        print_in_red(f"Unknown command: {command}")
        help_message()

if __name__ == "__main__":
    main()
