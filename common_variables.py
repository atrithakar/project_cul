'''
This file contains the common variables used in the project.
The purpose of this file is to make it easier to manage the variables that are used in multiple files.
'''
import appdirs

DEFAULT_URL = "https://cul-backend-fastapi-mongodb.onrender.com" # Default URL for the CUL backend, change to your local server address if needed
BASE_URL = "https://cul-backend-fastapi-mongodb.onrender.com" # Default URL for the CUL backend, change to your local server address if needed

# For debugging purposes, you can uncomment the following lines to use a local server
# DEFAULT_URL = "http://192.168.0.100:8000" # Default URL for the CUL backend, change to your local server address if needed
# BASE_URL = "http://192.168.0.100:8000" # Default URL for the CUL backend, change to your local server address if needed

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