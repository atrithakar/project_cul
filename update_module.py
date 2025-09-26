import os, json, urllib.request
from cache_and_install import check_cache_and_install
from colorful_outputs import print_in_green, print_in_red, print_in_yellow
from common_variables import BASE_URL, CACHE_DIR
from init import add_requirements
from helper_functions import parse_module, compare_versions
from install_module_2 import install, get_installed_version
from uninstall_module import uninstall

def update(module_name: str, registry: str = BASE_URL):
    '''
    Checks if the module is already installed and updates it to the latest version available on the server else gives a warning

    Args:
        module_name (str): The name of the module to update
    
    Returns:
        None

    Raises:
        None
    '''

    if "==" in module_name:
        module_name, _ = parse_module(module_name)
    
    registry = BASE_URL if not registry else registry
    latest_version_from_server = get_latest_version_str_from_backend(module_name, registry)
    latest_version_from_cache = get_latest_version_str_from_cache(module_name)
    current_installed_version = get_installed_version(module_name)
    server_error = False

    if current_installed_version == "":
        print_in_yellow(f"Warning: Module '{module_name}' not found in 'c_cpp_modules_dld'.")
        return

    if latest_version_from_server == "unknown":
        print(f"Unable to fetch the latest version of {module_name} from the server, trying to fetch from cache...")
        server_error = True

    if server_error and latest_version_from_cache == "unknown":
        print_in_red(f"Error: Unable to fetch the latest version of '{module_name} from the cache. Try again later or check the name of the module again.")
        return

    if not server_error:
        res = compare_versions(latest_version_from_server, current_installed_version)
        if res == -1 or res == 0:
            print_in_yellow(f"Module '{module_name}' is already up-to-date with the latest version available on the server.")
            return
        
    if latest_version_from_cache != "unknown":
        res = compare_versions(latest_version_from_cache, current_installed_version)
        if res == -1 or res == 0:
            print_in_yellow(f"Module '{module_name}' is already up-to-date with the latest version available in the cache.")
            return

    if server_error:
        if check_cache_and_install(module_name, latest_version_from_cache):
            add_requirements(module_name, latest_version_from_cache)
        return

    print(f"Updating {module_name}...")
    uninstall(module_name)
    
    if latest_version_from_server != "unknown":
        module_name = f"{module_name}=={latest_version_from_server}"
    
    install(module_name, registry=registry)
    print_in_green(f"Module '{module_name}' has been successfully updated to the latest version.")

def get_latest_version_str_from_backend(module_name: str, registry: str = BASE_URL):
    '''
    Fetches the latest version of the module from the server

    Args:
        module_name (str): The name of the module

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
        registry = BASE_URL if not registry else registry
        with urllib.request.urlopen(f"{registry}/get_latest_version/{module_name}") as response:
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

def get_latest_version_str_from_cache(module_name: str):
    '''
    Fetches the latest version of the specified module available in the cache

    Args:
        module_name (str): The name of the module

    Returns:
        str: The latest version of the module or 'unknown' if the module is not found

    Raises:
        FileNotFoundError: If the module is not found in the cache directory
        JSONDecodeError: If the JSON decoding fails
        Exception: If any unexpected error occurs
    '''
    try:
        versions_json_path = os.path.join(CACHE_DIR, module_name, "versions.json")
        if not os.path.isfile(versions_json_path):
            return "unknown"
        with open(versions_json_path, 'r') as f:
            versions_data = json.load(f)
            return versions_data.get("latest_version", "unknown")
    except FileNotFoundError:
        # print_in_yellow(f"Warning: Module '{module_name}' not found in cache.")
        return "unknown"
    except json.JSONDecodeError:
        print_in_red("Error reading JSON file. It may be corrupted.")
        return "unknown"
    except Exception as e:
        print_in_red(f"Unexpected error: {e}")
        return "unknown"
    