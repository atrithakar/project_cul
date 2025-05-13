'''
This file contains the common variables used in the project.
The purpose of this file is to make it easier to manage the variables that are used in multiple files.
'''
import appdirs

# BASE_URL = "https://culb.vercel.app"
DEFAULT_URL = "http://192.168.0.103:8000" # Local server for testing, change to your local server address
BASE_URL = "http://192.168.0.103:8000" # Local server for testing, change to your local server address

try:
    with open('.cul/cul_config.txt', 'r') as f:
        text = f.read().strip()
        BASE_URL = text if text else DEFAULT_URL

except FileNotFoundError:
    pass # Default to BASE_URL if file not found
except Exception as e:
    print(f"An unexpected error has occurred: {e}")

C_CPP_MODULES_DLD_DIR = "./c_cpp_modules_dld"
CACHE_DIR = appdirs.user_cache_dir("CUL", "CUL_CLI")
CUL_DIR = ".cul"