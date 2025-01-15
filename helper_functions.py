'''
This file contains the helper functions used in the project.
The purpose of this file is to make it easier to manage the functions that are used in multiple files.
These functions are the ones which are tiny and are used in multiple files.
'''

from colorful_outputs import print_in_red
import os
import chardet

def ensure_dir_exists(directory: str):
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

def parse_module(module_name_str: str):
    return module_name_str.split("==") if "==" in module_name_str else [module_name_str, ""]

def check_if_dir_exists(directory):
    return os.path.exists(directory)

def handle_req_file_ops(file_path: str, func: callable):
    try:
        raw_data = None
        with open(file_path,'rb') as f:
            raw_data = f.read()
        result = chardet.detect(raw_data)
        content = raw_data.decode(result['encoding'])
        for line in content.split('\n'):
            if(line == ''):
                continue
            func(line.strip())
    except FileNotFoundError:
        print_in_red(f"Error: {file_path} not found.")
    except Exception as e:
        print_in_red(f"Error: {e}")