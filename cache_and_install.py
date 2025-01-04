import shutil
import os
import appdirs
from common_variables import C_CPP_MODULES_DLD_DIR
from colorful_outputs import print_in_green, print_in_red
import json

CACHE_DIR = appdirs.user_cache_dir("CUL", "CUL_CLI")


def manage_versions_json(module_name):
    '''
    Manages the versions.json file for the specified module in the cache directory

    Args:
        module_name (str): The name of the module to manage/modify the versions.json file for

    Returns:
        None

    Raises:
        Exception: If any unexpected error occurs
    '''
    module_dir = os.path.join(CACHE_DIR, module_name)
    versions_file = os.path.join(module_dir, "versions.json")

    if not os.path.exists(module_dir):
        print(f"Module '{module_name}' does not exist in the cache.")
        return

    versions = [folder for folder in os.listdir(module_dir) if os.path.isdir(os.path.join(module_dir, folder))]

    if not versions:
        if os.path.exists(versions_file):
            os.remove(versions_file)
            print(f"Deleted empty versions.json for module '{module_name}'.")
        return

    versions.sort(key=lambda v: list(map(int, v.split("."))))
    
    versions_data = {
        "versions": versions,
        "latest_version": versions[-1]
    }

    with open(versions_file, "w") as f:
        json.dump(versions_data, f, indent=4)
    
    # print(f"versions.json for module '{module_name}' updated successfully.")

def cache_module(zip_ref, module_name, version='1.0.0'):
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
        
        # print_in_green(f"Module '{module_name} version {version}' has been successfully cached.")
    except Exception as e:
        print_in_red(f"Error caching module: {e}")

def check_cache_and_install(module_name, version=''):
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
    # cache_filepath = os.path.join(CACHE_DIR, f"{module_name}_v{version}")
    # print(f"First: {module_name}, {version}")
    cache_module_dir = os.path.join(CACHE_DIR, module_name)
    # print(f"Then, {cache_module_dir}")
    try:
        # installed_version = None
        if version == '':
            with open(os.path.join(cache_module_dir, "versions.json"), 'r') as f:
                versions_data = json.load(f)
                version = versions_data.get("latest_version")
                # print(f"Then in try->if, {module_name}, {version}")
        cache_version_dir = os.path.join(cache_module_dir, version)
        if os.path.isdir(os.path.join(C_CPP_MODULES_DLD_DIR, module_name)):
            # print(f"Then in try->if, {module_name}, {version}")
            shutil.rmtree(os.path.join(C_CPP_MODULES_DLD_DIR, module_name))
        if os.path.isdir(cache_version_dir):
            # print(f"Then in try->if, {module_name}, {version}")
            shutil.copytree(cache_version_dir, os.path.join(C_CPP_MODULES_DLD_DIR, module_name))
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
        FileNotFoundError: If the cache directory does not exist
        Exception: If any unexpected error occurs
    '''
    try:
        shutil.rmtree(CACHE_DIR)
        print_in_green("Cache cleared successfully.")
    except FileNotFoundError:
        print_in_red("Cache is already empty.")
    except Exception as e:
        print_in_red(f"Error clearing cache: {e}")