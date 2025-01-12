import os
import json
import urllib.request
import shutil
import io
import zipfile
from cache_and_install import check_cache_and_install, cache_module
from colorful_outputs import print_in_green, print_in_red, print_in_yellow
from common_variables import C_CPP_MODULES_DLD_DIR, BASE_URL, CACHE_DIR
from init import add_requirements, remove_requirements
from helper_functions import parse_module

def check_requirements_and_download(module_name, version='1.0.0'):
    '''
    Checks the requirements of the current module being downloaded and installs them if not already installed

    Args:
        module_name (str): The name of the module
        version (str): The version of the module

    Returns:
        None

    Raises:
        HTTPError: If the server returns an unsuccessful status code
        URLError: If the URL is invalid
        JSONDecodeError: If the JSON decoding fails
        KeyError: If the JSON response is missing keys
        Exception: If any unexpected error occurs
    '''
    try:
        version_json_path = os.path.join(C_CPP_MODULES_DLD_DIR, module_name, 'module_info.json')
        version_info = None
        with open(version_json_path, 'r') as f:
            version_info = json.load(f)
        
        requirements = version_info.get("requires", {})
        if not requirements:
            return None
        
        print_in_green(f"Installing requirements for {module_name}")
        for module in requirements:
            module_name, version = parse_module(module)
            if check_cache_and_install(module_name, version):
                print_in_green(f"Module '{module}' has been successfully installed from cache.")
                add_requirements(module_name, version)
                continue
            fetch_module(module_name, version)
    
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
    '''
    Downloads the module from the server and extracts it to the 'c_cpp_modules_dld' directory

    Args:
        module_name (str): The name of the module
        version (str): The version of the module

    Returns:
        None

    Raises:
        HTTPError: If the server returns an unsuccessful status code
        URLError: If the URL is invalid
        Exception: If any unexpected error occurs
    '''
    installed_version = check_cache_and_install(module_name,version)
    if installed_version:
        add_requirements(module_name, installed_version)
        check_requirements_and_download(module_name, installed_version)
        return
    
    try:
        zip_url = f"{BASE_URL}/files/{module_name}/{version}"
        
        req = urllib.request.Request(zip_url)
        # try:
        with urllib.request.urlopen(req) as response:
            if response.status != 200:
                raise Exception(f"HTTP {response.status}: Unable to fetch module.")
                
            zip_data = response.read()
        zip_stream = io.BytesIO(zip_data)
            
        module_dir = os.path.join(C_CPP_MODULES_DLD_DIR, module_name)
        os.makedirs(module_dir, exist_ok=True)
            
        with zipfile.ZipFile(zip_stream, 'r') as zip_ref:
            with zip_ref.open(f"module_info.json") as f:
                module_info = json.load(f)
                version = module_info.get("version")
                # print(installed_version)
                
            zip_ref.extractall(module_dir)
            print_in_green(f"Module '{module_name}' Version '{version}' has been successfully installed.")
            cache_module(zip_ref, module_name, version)
            add_requirements(module_name, version)
        check_requirements_and_download(module_name, installed_version)
    except urllib.error.HTTPError as e:
        error_message = e.read().decode()
        error_message = json.loads(error_message)
        print_in_red(f"Error: {error_message.get('error')}")
    except urllib.error.URLError as e:
        print_in_red(f"Error: Unable to connect to the server. Reason: {e.reason}")
    except Exception as e:
        print_in_red(f"Unexpected error Here: {e}")

def check_already_installed(module_name, version='1.0.0'):
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
    '''
    Splits the module name and version if the user has provided the version and installs the module

    Args:
        module_name (str): The name of the module to install

    Returns:
        None

    Raises:
        None
    '''
    module_name_, version = parse_module(module_name)
    if version:
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
    if os.path.isdir(module_path):
        try:
            shutil.rmtree(module_path)
            print_in_green(f"Successfully uninstalled {module_name}.")
            remove_requirements(module_name)
        except Exception as e:
            print_in_red(f"Error uninstalling module: {e}")
    else:
        print_in_yellow(f"Warning: Module '{module_name}' not found in 'c_cpp_modules_dld'.")

def update_module(module_name):
    '''
    Updates the module to the latest version available on the server

    Args:
        module_name (str): The name of the module to update

    Returns:
        None

    Raises:
        Exception: If there is an error while updating the module
    '''
    try:
        zip_url = f"{BASE_URL}/files/{module_name}/"
        req = urllib.request.Request(zip_url)

        with urllib.request.urlopen(req) as response:
            if response.status != 200:
                raise Exception(f"HTTP {response.status}: Unable to fetch module.")

            zip_data = response.read()
            zip_stream = io.BytesIO(zip_data)
            # print(zip_stream)
            with zipfile.ZipFile(zip_stream, 'r') as zip_ref:
                with zip_ref.open(f"module_info.json") as f:
                    module_info = json.load(f)
                    version = module_info.get("version")
                module_dir = os.path.join(C_CPP_MODULES_DLD_DIR, module_name)
                shutil.rmtree(module_dir)
                os.makedirs(module_dir, exist_ok=True)
                zip_ref.extractall(module_dir)
                print_in_green(f"Module '{module_name}' has been successfully updated.")
                add_requirements(module_name, version)
                cache_module(zip_ref, module_name, version)
    except Exception as e:
        print_in_red(f"Error: {e}")

def update(module_name):
    '''
    Checks if the module is already installed and updates it to the latest version available on the server else gives a warning

    Args:
        module_name (str): The name of the module to update
    
    Returns:
        None

    Raises:
        None
    '''
    
    latest_version_from_server = get_latest_version_str_from_backend(module_name)
    latest_version_from_cache = "unknown"
    server_error = False
    if latest_version_from_server == "unknown":
        print(f"Unable to fetch the latest version of {module_name} from the server, trying to fetch from cache...")
        server_error = True
        latest_version_from_cache = get_latest_version_str_from_cache(module_name)

    if latest_version_from_server <= get_current_installed_version(module_name):
        print_in_yellow(f"Module '{module_name}' is already up-to-date.")
        return

    if server_error and latest_version_from_cache == "unknown":
        print_in_red(f"Error: Unable to fetch the latest version of '{module_name} from the cache. Try again later'.")
        return

    if latest_version_from_cache <= get_current_installed_version(module_name):
        print_in_yellow(f"Module '{module_name}' is already up-to-date.")
        return

    if server_error:
        check_cache_and_install(module_name, latest_version_from_cache)
        return

    if(os.path.isdir(os.path.join(C_CPP_MODULES_DLD_DIR, module_name))):
        print(f"Updating {module_name}...")
        # fetch_module(module_name, update_called=True)
        update_module(module_name)
        # fetch_module(module_name)
    else:
        print_in_yellow(f"Warning: Library '{module_name}' not found in 'c_cpp_modules_dld'.")

def get_latest_version_str_from_backend(module_name):
    '''
    Fetches the latest version of the module from the server

    Args:
        None

    Returns:
        str: The latest version of the module

    Raises:
        HTTPError: If the server returns an unsuccessful status code
        URLError: If the URL is invalid
        JSONDecodeError: If the JSON decoding fails
        KeyError: If the JSON response is missing keys
        Exception: If any unexpected error occurs
    '''
    try:
        with urllib.request.urlopen(f"{BASE_URL}/latest_version/{module_name}") as response:
            if response.status != 200:
                raise urllib.error.HTTPError(f"{BASE_URL}/latest", response.status, f"Unable to fetch the latest version.", response.getheaders(), None)
            
            latest_data = response.read().decode()
            latest_info = json.loads(latest_data)
            return latest_info.get("latest", "unknown")
    except urllib.error.HTTPError as http_err:
        print_in_red(f"HTTP error: {http_err.code} {http_err.reason}")
        return "unknown"
    except urllib.error.URLError as url_err:
        print_in_red(f"URL error: {url_err.reason}")
        return "unknown"
    except json.JSONDecodeError:
        print_in_red("Failed to decode the JSON response. Please check the server response.")
        return "unknown"
    except KeyError as key_err:
        print_in_red(f"Key error: {key_err}")
        return "unknown"
    except Exception as e:
        print_in_red(f"Unexpected error: {e}")
    return "unknown"

def get_latest_version_str_from_cache(module_name):
    try:
        versions_json_path = os.path.join(CACHE_DIR, module_name, "versions.json")
        if not os.path.isfile(versions_json_path):
            return "unknown"
        with open(versions_json_path, 'r') as f:
            versions_data = json.load(f)
            return versions_data.get("latest_version", "unknown")
    except FileNotFoundError:
        print_in_yellow(f"Warning: Module '{module_name}' not found in cache.")
        return "unknown"
    except json.JSONDecodeError:
        print_in_red("Error reading JSON file. It may be corrupted.")
        return "unknown"
    except Exception as e:
        print_in_red(f"Unexpected error: {e}")
        return "unknown"
    
def get_current_installed_version(module_name):
    try:
        module_info_path = os.path.join(C_CPP_MODULES_DLD_DIR, module_name, "module_info.json")
        with open(module_info_path, 'r') as f:
            module_info = json.load(f)
            return module_info.get("version", "unknown")
    except FileNotFoundError:
        print_in_yellow(f"Warning: Module '{module_name}' not found in 'c_cpp_modules_dld'.")
        return "unknown"
    except json.JSONDecodeError:
        print_in_red("Error reading JSON file. It may be corrupted.")
        return "unknown"
    except Exception as e:
        print_in_red(f"Unexpected error: {e}")
        return "unknown"