import os
import json
import urllib.request
import io
import zipfile
from cache_and_install import *
from colorful_outputs import *
from common_variables import C_CPP_MODULES_DLD_DIR, BASE_URL
from init import add_requirements

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
                add_requirements(module.split("==")[0], module.split("==")[1])
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

    if check_cache_and_install(module_name, version):
        add_requirements(module_name, version)
        check_requirements_and_download(module_name, version)
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

def update_module(module_name):
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
    if(os.path.isdir(os.path.join(C_CPP_MODULES_DLD_DIR, module_name))):
        print(f"Updating {module_name}...")
        # fetch_module(module_name, update_called=True)
        update_module(module_name)
        # fetch_module(module_name)
    else:
        print_in_yellow(f"Warning: Library '{module_name}' not found in 'c_cpp_modules_dld'.")