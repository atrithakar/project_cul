'''
This file contains the common variables used in the project.
The purpose of this file is to make it easier to manage the variables that are used in multiple files.
'''
import appdirs

BASE_URL = "https://culb.vercel.app"
# BASE_URL = "http://192.168.0.104:5000"
C_CPP_MODULES_DLD_DIR = "./c_cpp_modules_dld"
CACHE_DIR = appdirs.user_cache_dir("CUL", "CUL_CLI")
CUL_DIR = ".cul"