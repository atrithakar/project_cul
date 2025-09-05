import os, json, io, zipfile, urllib.request
from cache_and_install import check_cache_and_install, cache_module
from colorful_outputs import print_in_green, print_in_red, print_in_yellow
from common_variables import C_CPP_MODULES_DLD_DIR, BASE_URL
from init import add_requirements
from helper_functions import parse_module
from checksum import verify_checksum
from uninstall_module import uninstall

def fetch_module_from_server(module_name: str, version: str = '', registry: str = BASE_URL, save_dir: str = C_CPP_MODULES_DLD_DIR) -> bool:
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
        urlib.error.HTTPError: If the server returns an unsuccessful status code
        urlib.error.URLError: If the URL is invalid
        zipfile.BadZipFile: If the downloaded file is not a valid zip file
        json.JSONDecodeError: If the JSON decoding fails
        Exception: If any unexpected error occurs during fetching or saving the module
    '''
    try:
        url = f"{registry}/files/{module_name}/{version}"
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
        
        if not verify_checksum(save_dir):
            print_in_red(f"Checksum verification failed for module '{module_name}'.\nThe module may be corrupted or tampered.")
            # remove_module_from_cache(module_name, version)
            # shutil.rmtree(save_dir)
            # return False
            '''
            If code execution reaches in this if block, it means that the checksum verification failed for that module.
            In a normal scenario, we'd like to remove the module from the cache and uninstall it to save user from corrupted or tampered files.
            But currently we are not doing so because the backend is hosted on Render and from our debugging we havve found that Render may be altering file endings causing checksum verification to fail.
            So, temporarily we are not removing the module from the cache and uninstalling it if checksum verification fails because Render altering file endings doesn't inherently mean that the module is corrupted or tampered.
            As soon as we find a better way to handle this, we will uncomment the above code and remove the module from the cache and uninstall it if checksum verification fails.
            '''
        
        fetch_dependency(module_name, module_name, save_dir, version)
        
        return True
    
    except urllib.error.HTTPError as e:
        print_in_red(f"HTTP Error {e.code} while fetching module '{module_name}': {e.reason}")
        return False    
    except urllib.error.URLError as e:
        print_in_red(f"URL Error while fetching module '{module_name}': {e.reason}")
        return False
    except zipfile.BadZipFile:
        print_in_red(f"Error: The downloaded file for module '{module_name}' is not a valid zip file.")
        return False
    except json.JSONDecodeError:
        print_in_red(f"Error: Failed to decode JSON for module '{module_name}'. The module_info.json file may be corrupted.")
        return False
    except Exception as e:
        print_in_red(f"An error occurred while fetching module '{module_name}': {e}")
        return False


def fetch_module_from_cache(module_name: str, version: str = '', save_dir: str = C_CPP_MODULES_DLD_DIR) -> bool:
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
    '''
    Fetches the dependencies of a module after it has been installed.

    Args:
        module_name (str): The name of the module whose dependencies are to be fetched
        parent_module_name (str): The name of the parent module that requires this dependency
        save_dir (str): The directory where the module is saved
        version (str): The version of the module. If empty, fetches the latest version.

    Returns:
        None

    Raises:
        None
    '''
    with open(os.path.join(save_dir, "module_info.json"), 'r') as f:
        module_info = json.load(f)
        dependencies = module_info.get("requires", [])

    for dependency in dependencies:
        dep_name, dep_ver = parse_module(dependency)
        nested_dep_dir = os.path.join(save_dir, "c_cpp_modules_dld")
        
        if fetch_module_from_cache(dep_name, dep_ver, nested_dep_dir):
            continue
        elif fetch_module_from_server(dep_name, dep_ver, save_dir=nested_dep_dir):
            continue
        else:
            print_in_red(f"Failed to fetch dependency '{dep_name}' required by '{parent_module_name}'.")


def get_installed_version(module_name: str) -> str:
    '''
    Returns the installed version of the specified module.

    Args:
        module_name (str): The name of the module

    Returns:
        str: The installed version of the module, or an empty string if not installed or on error

    Raises:
        None
    '''
    try:
        with open(os.path.join(C_CPP_MODULES_DLD_DIR, module_name, "module_info.json"), 'r') as f:
            module_info = json.load(f)
            return module_info.get("version", "")
    except (json.JSONDecodeError, IOError, FileNotFoundError):
        return ""


def install(module: str, registry: str = BASE_URL):
    '''
    Installs the specified module by checking if it's already installed, fetching it from cache or server, and handling dependencies.

    Args:
        module (str): The name of the module to install, optionally with version (e.g., "module_name==1.0.0")
        registry (str): The registry URL to fetch the module from. Defaults to BASE_URL.

    Returns:
        None

    Raises:
        None
    '''
    module_name, module_version = parse_module(module)
    installed_version = get_installed_version(module_name)
    registry = BASE_URL if not registry else registry

    if installed_version:
        print_in_yellow(f"Module '{module_name}' is already installed with version '{installed_version}'.")
        print("Would you like to reinstall it? (y/n): ", end="")
        choice = input().strip().lower()
        if choice == '':
            return
        choice = choice[0]
        if choice == 'y':
            uninstall(module_name)
        else:
            return

    
    if fetch_module_from_cache(module_name, module_version) or fetch_module_from_server(module_name, module_version, registry):
        installed_version = get_installed_version(module_name)
        add_requirements(module_name, installed_version)
        return
        
    print_in_red(f"Failed to install module '{module_name}'.")
