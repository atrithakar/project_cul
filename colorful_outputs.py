
from colorama import Fore, init

init(autoreset=True)

def print_in_red(message):
    print(Fore.RED + message)

def print_in_yellow(text):
    print(Fore.YELLOW + text)

def print_in_green(text):
    print(Fore.GREEN + text)
