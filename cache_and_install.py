import shutil
import os
from common_variables import C_CPP_MODULES_DLD_DIR, CACHE_DIR
from colorful_outputs import print_in_green, print_in_red, print_in_yellow
import json
import zipfile

def manage_versions_json(module_name: str):
    '''
    Manages the versions.json file for the specified module in the cache directory

    Args:
        module_name (str): The name of the module to manage/modify the versions.json file for

    Returns:
        None

    Raises:
        Exception: If any unexpected error occurs during dumping the versions data to the versions.json file
    '''
    module_dir = os.path.join(CACHE_DIR, module_name)
    versions_file = os.path.join(module_dir, "versions.json")

    if not os.path.exists(module_dir):
        print(f"Module '{module_name}' does not exist in the cache.")
        return

    versions = [folder for folder in os.listdir(module_dir) if os.path.isdir(os.path.join(module_dir, folder))]

    if not versions and os.path.exists(versions_file):
        os.remove(versions_file)
        print(f"Deleted empty versions.json for module '{module_name}'.")
        return

    versions.sort(key=lambda v: list(map(int, v.split("."))))
    
    versions_data = {
        "versions": versions,
        "latest_version": versions[-1]
    }

    try:
        with open(versions_file, "w") as f:
            json.dump(versions_data, f, indent=4)
    except Exception as e:
        print_in_red(f"Error updating versions.json for module '{module_name}': {e}")

def manage_cached_json(module_name: str, version: str):
    '''
    Manages the cached.json file in the cache directory to reflect the cached modules and versions.

    Args:
        module_name (str): The name of the module to manage/modify the cached.json file for
        version (str): The version of the module to manage/modify the cached.json file for

    Returns:
        None

    Raises:
        Exception: If any unexpected error occurs during updating the cached.json file
        JSONDecodeError: If the JSON decoding fails while reading the cached.json file
    '''
    cached_file = os.path.join(CACHE_DIR, "cached.json")
    cached_data = {}
        
    if os.path.exists(cached_file):
        with open(cached_file, "r") as f:
            try:
                cached_data = json.load(f)
            except json.JSONDecodeError:
                print_in_red("Error reading cached.json file. It may be corrupted.")

    if module_name not in cached_data:
        cached_data[module_name] = []
    if version not in cached_data[module_name]:
        cached_data[module_name].append(version)
        cached_data[module_name].sort(key=lambda v: list(map(int, v.split("."))))
    
    try:
        with open(cached_file, "w") as f:
            json.dump(cached_data, f, indent=4)
    except Exception as e:
        print_in_red(f"Error updating cached.json: {e}")


def cache_module(zip_ref: zipfile.ZipFile, module_name: str, version: str = '1.0.0'):
    '''
    Cache the module along with its version in the cache directory

    Args:
        zip_ref (ZipFile): The ZipFile object of the module to cache
        module_name (str): The name of the module to cache
        version (str): The version of the module to cache

    Returns:
        None

    Raises:
        Exception: If any unexpected error occurs
    '''
    try:
        os.makedirs(CACHE_DIR, exist_ok=True)
        # cache_filepath = os.path.join(CACHE_DIR, f"{module_name}_v{version}")
        cached_module_dir = os.path.join(CACHE_DIR, module_name)
        cached_version_dir = os.path.join(cached_module_dir, version)
        os.makedirs(cached_module_dir, exist_ok=True)
        os.makedirs(cached_version_dir, exist_ok=True)
        zip_ref.extractall(cached_version_dir)
        
        manage_versions_json(module_name)
        manage_cached_json(module_name, version)
        
        # print_in_green(f"Module '{module_name} version {version}' has been successfully cached.")
    except Exception as e:
        print_in_red(f"Error caching module: {e}")

def check_cache_and_install(module_name: str, version: str = ''):
    '''
    Checks if the module of user specified version is available in the cache and installs it if found

    Args:
        module_name (str): The name of the module to install
        version (str): The version of the module to install

    Returns:
        version (str): The version of the module that was installed from the cache
        False (bool): Otherwise

    Raises:
        FileNotFoundError: If the cache directory does not exist
        Exception: If any unexpected error occurs
    '''

    cache_module_dir = os.path.join(CACHE_DIR, module_name)
    try:
        # installed_version = None
        if version == '':
            with open(os.path.join(cache_module_dir, "versions.json"), 'r') as f:
                versions_data = json.load(f)
                version = versions_data.get("latest_version")
        cache_version_dir = os.path.join(cache_module_dir, version)
        # if os.path.isdir(os.path.join(C_CPP_MODULES_DLD_DIR, module_name)):
            # shutil.rmtree(os.path.join(C_CPP_MODULES_DLD_DIR, module_name))
        if os.path.isdir(cache_version_dir):
            shutil.copytree(cache_version_dir, os.path.join(C_CPP_MODULES_DLD_DIR, module_name), dirs_exist_ok=True)
            print_in_green(f"Module '{module_name}' Version '{version}' has been successfully installed from cache.")
            return version
        return False
    except FileNotFoundError:
        # print_in_red(f"Error: Module '{module_name}' not found in cache.")
        return False
    except Exception as e:
        print_in_red(f"Unexpected Error: {e}")
        return False

def clear_cache():
    '''
    Clears the cache directory

    Args:
        None
    
    Returns:
        None

    Raises:
        FileNotFoundError: If the cache is already empty
        Exception: If any unexpected error occurs
    '''
    try:
        shutil.rmtree(CACHE_DIR)
        print_in_green("Cache cleared successfully.")
    except FileNotFoundError:
        print_in_yellow("Warning: Cache is already empty.")
    except Exception as e:
        print_in_red(f"Error clearing cache: {e}")

def show_cache():
    '''
    Shows the contents of the cache directory

    Args:
        None

    Returns:
        None

    Raises:
        FileNotFoundError: If the cache directory does not exist
        Exception: If any unexpected error occurs
    '''
    try:
        cache_file_path = os.path.join(CACHE_DIR, "cached.json")
        cached_data = {}
        with open(cache_file_path, "r") as f:
            cached_data = json.load(f)
        print("Cache contents:")
        for module, versions in cached_data.items():
            print(f"  {module}:")
            for version in versions:
                print(f"    - v{version}")
            print()
    except FileNotFoundError:
        print("Cache is empty.")
    except Exception as e:
        print_in_red(f"Error showing cache: {e}")

def remove_module_from_cache(module_name: str) -> None:
    '''
    Removes the specified module from the cache directory

    Args:
        module_name (str): The name of the module to remove from the cache

    Returns:
        None

    Raises:
        FileNotFoundError: If the module is not found in the cache
        Exception: If any unexpected error occurs
    '''
    try:
        shutil.rmtree(os.path.join(CACHE_DIR, module_name))
        # print_in_green(f"Module '{module_name}' removed from cache.")

        with open(os.path.join(CACHE_DIR, "cached.json"), "r") as f:
            cached_data = json.load(f)

        if module_name in cached_data:
            del cached_data[module_name]
            with open(os.path.join(CACHE_DIR, "cached.json"), "w") as f:
                json.dump(cached_data, f, indent=4)
    except FileNotFoundError:
        print_in_yellow(f"Module '{module_name}' not found in cache.")
    except Exception as e:
        print_in_red(f"Error removing module from cache: {e}")