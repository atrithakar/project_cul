'''
This file contains the helper functions used in the project.
The purpose of this file is to make it easier to manage the functions that are used in multiple files.
These functions are the ones which are tiny and are used in multiple files.
'''
from colorful_outputs import print_in_red
import os
import chardet

def parse_module(module_name_str: str):
    '''
    Parses the module name and version from the input string.

    Args:
        module_name_str (str): The input string containing the module name and version

    Returns:
        list: A list containing the module name and version

    Raises:
        None
    '''
    return module_name_str.split("==") if "==" in module_name_str else [module_name_str, ""]

def handle_req_file_ops(file_path: str, func: callable):
    '''
    Handles the operations on the requirements file, and executes the specified function on each line of the file, abstracting the encoding detection and file reading.

    Args:
        file_path (str): The path to the requirements file
        func (callable): The function to be executed

    Returns:
        None

    Raises:
        FileNotFoundError: If the file is not found
        Exception: If any unexpected error occurs
    '''
    try:
        raw_data = None
        with open(file_path,'rb') as f:
            raw_data = f.read()
        result = chardet.detect(raw_data)
        content = raw_data.decode(result['encoding'])
        for line in content.split('\n'):
            if line.isspace() or line == '':
                continue
            func(line.strip())
    except FileNotFoundError:
        print_in_red(f"Error: {file_path} not found.")
    except Exception as e:
        print_in_red(f"Error: {e}")