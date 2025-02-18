from colorama import Fore, init
import os
import shutil
from common_variables import CUL_DIR
from datetime import datetime

init(autoreset=True)

def print_in_red(text: str):
    '''
    Prints the message in red color and writes it to the errors.log file in the CUL_DIR directory.

    Args:
        text (str): The message to print

    Returns:
        None

    Raises:
        FileNotFoundError: If the errors.log file is not found
        Exception: If any unexpected error occurs
    '''
    print(Fore.RED + text)

    os.makedirs(CUL_DIR, exist_ok=True)
    try:
        file_size_in_MB = os.path.getsize(os.path.join(CUL_DIR, "errors.log")) / (1024 * 1024)
        # file_size = os.path.getsize(os.path.join(CUL_DIR, "errors.log")) # used for testing and debugging

        if file_size_in_MB >= 10:
            with open (os.path.join(CUL_DIR, "errors.log"), 'w') as f:
                f.write("")

        with open(os.path.join(CUL_DIR, "errors.log"), 'a') as f:
            timestamp = datetime.now().strftime("%I:%M %p %m/%d/%Y")
            f.write(f"[{timestamp}]: {text}\n")

    except FileNotFoundError:
        with open(os.path.join(CUL_DIR, "errors.log"), 'w') as f:
            timestamp = datetime.now().strftime("%I:%M %p %m/%d/%Y")
            f.write(f"[{timestamp}]: FILE CREATED\n")
            f.write(f"[{timestamp}]: {text}\n")

    except Exception as e:
        print_in_red(f"Unexpected error: {e}")

def print_in_yellow(text: str):
    '''
    Prints the message in yellow color and writes it to the warnings.log file in the CUL_DIR directory.

    Args:
        text (str): The message to print

    Returns:
        None

    Raises:
        FileNotFoundError: If the warnings.log file is not found
        Exception: If any unexpected error
    '''
    print(Fore.YELLOW + text)

    os.makedirs(CUL_DIR, exist_ok=True)
    try:
        file_size_in_MB = os.path.getsize(os.path.join(CUL_DIR, "warnings.log")) / (1024 * 1024)
        # file_size = os.path.getsize(os.path.join(CUL_DIR, "warnings.log")) # used for testing and debugging

        if file_size_in_MB >= 10:
            with open (os.path.join(CUL_DIR, "warnings.log"), 'w') as f:
                f.write("")

        with open(os.path.join(CUL_DIR, "warnings.log"), 'a') as f:
            timestamp = datetime.now().strftime("%I:%M %p %m/%d/%Y")
            f.write(f"[{timestamp}]: {text}\n")

    except FileNotFoundError:
        with open(os.path.join(CUL_DIR, "warnings.log"), 'w') as f:
            timestamp = datetime.now().strftime("%I:%M %p %m/%d/%Y")
            f.write(f"[{timestamp}]: FILE CREATED\n")
            f.write(f"[{timestamp}]: {text}\n")

    except Exception as e:
        print_in_red(f"Unexpected error: {e}")

def print_in_green(text: str):
    '''
    Prints the message in green color. Used for success messages.

    Args:
        text (str): The message to print

    Returns:
    None

    Raises:
    None
    '''
    print(Fore.GREEN + text)
