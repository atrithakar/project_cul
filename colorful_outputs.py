
from colorama import Fore, init

init(autoreset=True)

def print_in_red(message):
    '''
    Prints the message in red color. Used for error messages.

    Args:
    None

    Returns:
    None

    Raises:
    None
    '''
    print(Fore.RED + message)

def print_in_yellow(text):
    '''
    Prints the message in yellow color. Used for warning messages.

    Args:
    None

    Returns:
    None

    Raises:
    None
    '''
    print(Fore.YELLOW + text)

def print_in_green(text):
    '''
    Prints the message in green color. Used for success messages.

    Args:
    None

    Returns:
    None

    Raises:
    None
    '''
    print(Fore.GREEN + text)
