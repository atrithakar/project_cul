import os
import json
import urllib.request
import shutil
import io
import zipfile
from cache_and_install import check_cache_and_install, cache_module, remove_module_from_cache
from colorful_outputs import print_in_green, print_in_red, print_in_yellow
from common_variables import C_CPP_MODULES_DLD_DIR, BASE_URL
from init import add_requirements, remove_requirements
from helper_functions import parse_module
from search_module import fuzzy_search_module
from checksum import verify_checksum

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

        print(f"Installing requirements for {module_name}...")
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

def fetch_module(module_name: str, version: str = '', registry: str = BASE_URL):
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
        zip_url = f"{registry}/files/{module_name}/{version}"
        
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
        if e.code == 404:
            print_in_yellow(f"Module '{module_name}'" + (f" Version '{version}'" if version else "") + " not found.")

            modules = fuzzy_search_module(module_name, registry=registry)
            if len(modules) == 0:
                return

            print("Did you mean:")
            for i, module in enumerate(modules, start=1):
                print(f"{i}. {module}")
            print("Run 'cul search <module_name>' to get detailed info.")
            print("Run 'cul install <module_name>' to install the module.")    
            return
        print_in_red(f"Error: {error_message.get('error')}")
    except urllib.error.URLError as e:
        print_in_red(f"Error: Unable to connect to the server. Reason: {e.reason}")
    except json.JSONDecodeError as e:
        print_in_red(f"Error: {e}")
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

def install(module_name: str, registry: str = BASE_URL):
    '''
    Splits the module name and version if the user has provided the version and installs the module

    Args:
        module_name (str): The name of the module to install

    Returns:
        None

    Raises:
        None
    '''
    registry = BASE_URL if not registry else registry
    module_name_, version = parse_module(module_name)
    if version:
        if check_already_installed(module_name_, version):
            print_in_yellow(f"Module '{module_name_}' Version '{version}' is already installed.")
            return

        print(f"Installing {module_name_} Version {version}...")
        fetch_module(module_name_, version, registry)
    else:
        if check_already_installed(module_name):
            print_in_yellow(f"Module '{module_name}' is already installed.")
            return

        fetch_module(module_name=module_name, registry=registry)

    if os.path.isdir(os.path.join(C_CPP_MODULES_DLD_DIR, module_name_)):
        print(f"Verifying {module_name_}...")
        if not verify_checksum(os.path.join(C_CPP_MODULES_DLD_DIR, module_name_)):
            print_in_red(f"Checksum verification failed for {module_name_}.")
            remove_module_from_cache(module_name_)
            shutil.rmtree(os.path.join(C_CPP_MODULES_DLD_DIR, module_name_))
            print_in_red(f"Module '{module_name_}' has been removed from the cache and uninstalled.")
            return
        
        if os.path.exists(os.path.join(C_CPP_MODULES_DLD_DIR, module_name_, "checksum.txt")):
            os.remove(os.path.join(C_CPP_MODULES_DLD_DIR, module_name_, "checksum.txt"))
        
        print_in_green(f"Module '{module_name_}' has been successfully verified")


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

    if not os.path.isdir(module_path):
        print_in_yellow(f"Warning: Module '{module_name}' not found in 'c_cpp_modules_dld'.")
        return

    try:
        shutil.rmtree(module_path)
        print_in_green(f"Successfully uninstalled {module_name}.")
        remove_requirements(module_name)
    except Exception as e:
        print_in_red(f"Error uninstalling module: {e}")
