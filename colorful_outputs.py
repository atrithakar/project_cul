
from colorama import Fore, init

init(autoreset=True)

def print_in_red(text: str):
    '''
    Prints the message in red color. Used for error messages.

    Args:
        text (str): The message to print

    Returns:
    None

    Raises:
    None
    '''
    print(Fore.RED + text)

def print_in_yellow(text: str):
    '''
    Prints the message in yellow color. Used for warning messages.

    Args:
        text (str): The message to print

    Returns:
    None

    Raises:
    None
    '''
    print(Fore.YELLOW + text)

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
