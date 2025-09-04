import os
import json
import urllib.request
import shutil
import io
import zipfile
from cache_and_install import check_cache_and_install, cache_module, remove_module_from_cache
from colorful_outputs import print_in_green, print_in_red, print_in_yellow
from common_variables import C_CPP_MODULES_DLD_DIR, BASE_URL
from init import add_requirements
from helper_functions import parse_module
from search_module import fuzzy_search_module
from checksum import verify_checksum

def fetch_module_from_server(module_name: str, version: str = '', registry: str = BASE_URL, save_dir: str = C_CPP_MODULES_DLD_DIR):
    '''
    Fetches the specified module from the server and saves it to the specified directory.

    Args:
        module_name (str): The name of the module to fetch
        version (str): The version of the module to fetch. If empty, fetches the latest version.
        registry (str): The registry URL to fetch the module from. Defaults to BASE_URL.
        save_dir (str): The directory to save the fetched module to. Defaults to C_CPP_MODULES_DLD_DIR.

    Returns:
        bool: True if the module was fetched successfully, False otherwise.

    Raises:
        Exception: If any unexpected error occurs during fetching or saving the module
    '''
    try:
        url = f"{registry}/files/{module_name}/{version}"
        # if version:
        #     url += f"/{version}"

        save_dir = os.path.join(save_dir, module_name)
        
        print(f"Fetching module '{module_name}' from {url}...")
        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                print_in_red(f"Failed to fetch module '{module_name}'. Server responded with status code {response.status}.")
                return False
            
            zip_data = response.read()
            zip_stream = io.BytesIO(zip_data)
            with zipfile.ZipFile(zip_stream, 'r') as zip_ref:
                with zip_ref.open(f"module_info.json") as f:
                    module_info = json.load(f)
                    version = module_info.get("version")
                # print(installed_version)
                
                zip_ref.extractall(save_dir)
                cache_module(zip_ref, module_name, version)
               
        print_in_green(f"Module '{module_name}' fetched and saved to '{save_dir}'.")
        fetch_dependency(module_name, module_name, save_dir, version)
        
        return True
    
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print_in_yellow(f"Module '{module_name}'" + (f" Version '{version}'" if version else "") + " not found on the server.")

            modules = fuzzy_search_module(module_name, registry=registry)
            if len(modules) == 0:
                return

            print("Did you mean:")
            for i, module in enumerate(modules, start=1):
                print(f"{i}. {module}")
            print("Run 'cul search <module_name>' to get detailed info.")
            print("Run 'cul install <module_name>' to install the module.")    
            return
        else:
            print_in_red(f"HTTP Error {e.code} while fetching module '{module_name}': {e.reason}")
        return False    
    except urllib.error.URLError as e:
        print_in_red(f"URL Error while fetching module '{module_name}': {e.reason}")
        return False
    except Exception as e:
        print_in_red(f"An error occurred while fetching module '{module_name}': {e}")
        return False


def fetch_module_from_cache(module_name: str, version: str = '', save_dir: str = C_CPP_MODULES_DLD_DIR):
    '''
    Fetches the specified module from the local cache and saves it to the specified directory.

    Args:
        module_name (str): The name of the module to fetch
        version (str): The version of the module to fetch. If empty, fetches the latest version.
        save_dir (str): The directory to save the fetched module to. Defaults to C_CPP_MODULES_DLD_DIR.

    Returns:
        bool: True if the module was fetched successfully, False otherwise.

    Raises:
        Exception: If any unexpected error occurs during fetching or saving the module
    '''
    try:
        print(f"Fetching module '{module_name}' from cache...")
        save_dir = os.path.join(save_dir, module_name)
        cached_path = check_cache_and_install(module_name, version, save_dir)
        if cached_path:
            print_in_green(f"Module '{module_name}' fetched from cache and saved to '{cached_path}'.")
            fetch_dependency(module_name, module_name, save_dir, version)
            return True
        else:
            print_in_red(f"Module '{module_name}' not found in cache.")
            return False
    
    except Exception as e:
        print_in_red(f"An error occurred while fetching module '{module_name}' from cache: {e}")
        return False
    
def fetch_dependency(module_name: str, parent_module_name: str, save_dir: str, version: str = ''):
    # Use the actual save_dir instead of manipulating C_CPP_MODULES_DLD_DIR
    with open(os.path.join(save_dir, "module_info.json"), 'r') as f:
        module_info = json.load(f)
        dependencies = module_info.get("requires", [])

    for dependency in dependencies:
        print("---------" + dependency + "---------")
        dep_name, dep_ver = parse_module(dependency)

        # Create proper nested dependency path
        nested_dep_dir = os.path.join(save_dir, "c_cpp_modules_dld")
        
        if fetch_module_from_cache(dep_name, dep_ver, nested_dep_dir):
            continue
        elif fetch_module_from_server(dep_name, dep_ver, save_dir=nested_dep_dir):
            continue
        else:
            print_in_red(f"Failed to fetch dependency '{dep_name}' required by '{parent_module_name}'.")

    # fetch_module_from_cache(module_name, version, os.path.join(save_dir, C_CPP_MODULES_DLD_DIR[2:], module_name))

def check_already_installed(module_name: str, version: str = '1.0.0'):
    '''
    Checks if the module user is trying to install is already installed or not

    Args:
        module_name (str): The name of the module
        version (str): The version of the module

    Returns:
        bool: True if the module is already installed, False otherwise

    Raises:
        None
    '''
    module_exists = os.path.isdir(os.path.join(C_CPP_MODULES_DLD_DIR, module_name))
    version_exists = False

    if not module_exists:
        return False

    try:
        with open(os.path.join(C_CPP_MODULES_DLD_DIR, module_name, "module_info.json"), 'r') as f:
            module_info = json.load(f)
            version_exists = module_info.get("version") == version
        return module_exists and version_exists
    except (json.JSONDecodeError, IOError):
        # print(json.JSONDecodeError)
        # print(IOError)
        return False

def get_installed_version(module_name: str):
    try:
        with open(os.path.join(C_CPP_MODULES_DLD_DIR, module_name, "module_info.json"), 'r') as f:
            module_info = json.load(f)
            return module_info.get("version", "")
    except (json.JSONDecodeError, IOError):
        return ""


def install(module: str, registry: str = BASE_URL):

    module_name, module_version = parse_module(module)

    if check_already_installed(module_name, module_version):
        print_in_yellow(f"Module '{module_name}' is already installed.")
        return
    
    if fetch_module_from_cache(module_name, module_version) or fetch_module_from_server(module_name, module_version, registry):
        installed_version = get_installed_version(module_name)
        add_requirements(module_name, installed_version)
        return
    
    # if fetch_module_from_server(module_name, module_version, registry):
    #     installed_version = get_installed_version(module_name)
    #     add_requirements(module_name, installed_version)
    #     return
    
    
    print_in_red(f"Failed to install module '{module_name}'.")

if __name__ == "__main__":
    # Example usage
    # fetch_module_from_server("test_module_5")
    # print(check_already_installed("test_module_5", "1.0.1"))
    # fetch_module_from_cache("test_module_1", save_dir="./hello")
    install("test_module_9")
    modules = fuzzy_search_module("test_module_4")
    print(modules)