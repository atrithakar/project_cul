import shutil
import os
import appdirs
from common_variables import C_CPP_MODULES_DLD_DIR

CACHE_DIR = appdirs.user_cache_dir("CUL", "CUL_CLI")

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