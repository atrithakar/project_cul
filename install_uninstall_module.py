import os
import json
import urllib.request
import shutil
import io
import zipfile
from cache_and_install import check_cache_and_install, cache_module
from colorful_outputs import print_in_green, print_in_red, print_in_yellow
from common_variables import C_CPP_MODULES_DLD_DIR, BASE_URL
from init import add_requirements, remove_requirements
from helper_functions import parse_module

def check_requirements_and_download(module_name: str, version: str = '1.0.0'):
    '''
    Checks the requirements of the current module being downloaded and installs them if not already installed

    Args:
        module_name (str): The name of the module
        version (str): The version of the module

    Returns:
        None

    Raises:
        FileNotFoundError: If the module_info.json is not found
        JSONDecodeError: If the JSON decoding fails
        KeyError: If the JSON response is missing keys
        Exception: If any unexpected error occurs
    '''
    try:
        version_json_path = os.path.join(C_CPP_MODULES_DLD_DIR, module_name, 'module_info.json')
        version_info = None

        # Check if the module_info.json exists
        if not os.path.exists(version_json_path):
            raise FileNotFoundError(f"module_info.json not found for {module_name}. Cannot check requirements.")

        with open(version_json_path, 'r') as f:
            version_info = json.load(f)

        # Get requirements from module_info.json
        requirements = version_info.get("requires", {})
        if not requirements:
            return None

        print_in_green(f"Installing requirements for {module_name}...")
        for module in requirements:
            module_name, version = parse_module(module)

            # Install from cache or server
            if check_cache_and_install(module_name, version):
                print_in_green(f"Module '{module}' successfully installed from cache.")
                add_requirements(module_name, version)
                check_requirements_and_download(module_name, version)
            else:
                print(f"Installing {module} from server...")
                fetch_module(module_name, version)
    except FileNotFoundError as e:
        print_in_red(f"Error: {e}")
    except KeyError as e:
        print_in_red(f"Error: {e}")
    except json.JSONDecodeError as e:
        print_in_red(f"Error: {e}")
    except Exception as e:
        print_in_red(f"Unexpected error while resolving requirements for {module_name}: {e}")

def fetch_module(module_name: str, version: str = ''):
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
        check_requirements_and_download(module_name, version)
    except urllib.error.HTTPError as e:
        error_message = e.read().decode()
        error_message = json.loads(error_message)
        print_in_red(f"Error: {error_message.get('error')}")
    except urllib.error.URLError as e:
        print_in_red(f"Error: Unable to connect to the server. Reason: {e.reason}")
    except Exception as e:
        print_in_red(f"Unexpected error Here: {e}")

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

def install(module_name: str):
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
    if os.path.isdir(module_path):
        try:
            shutil.rmtree(module_path)
            print_in_green(f"Successfully uninstalled {module_name}.")
            remove_requirements(module_name)
        except Exception as e:
            print_in_red(f"Error uninstalling module: {e}")
    else:
        print_in_yellow(f"Warning: Module '{module_name}' not found in 'c_cpp_modules_dld'.")
