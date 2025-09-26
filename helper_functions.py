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

def handle_req_file_ops(file_path: str, func: callable, registry: str = None):
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
        if registry and (func.__name__ == 'install' or func.__name__ == 'update'):
            for line in content.split('\n'):
                if line.isspace() or line == '':
                    continue
                func(line.strip(), registry)
            return
            
        for line in content.split('\n'):
                if line.isspace() or line == '':
                    continue
                func(line.strip())
        
    except FileNotFoundError:
        print_in_red(f"Error: {file_path} not found.")
    except Exception as e:
        print_in_red(f"Error: {e}")
    
def compare_versions(version1: str, version2: str) -> int:
    '''
    Compares two semantic version strings.

    Args:
        version1 (str): The first semantic version string (e.g., "1.2.3")
        version2 (str): The second semantic version string (e.g., "1.2.4")

    Returns:
        int: -1 if version1 < version2,
              0 if version1 == version2,
              1 if version1 > version2

    Raises:
        ValueError: If either version string is not in the correct format
    '''
    try:
        v1_tuple = tuple(map(int, version1.split('.')))
        v2_tuple = tuple(map(int, version2.split('.')))
    except ValueError:
        raise ValueError(f"Invalid version format. Expected format: 'X.Y.Z' where X, Y, and Z are integers.")


    if v1_tuple < v2_tuple:
        return -1
    elif v1_tuple > v2_tuple:
        return 1
    else:
        return 0