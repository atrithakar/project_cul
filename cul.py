import sys
from colorful_outputs import print_in_red
from cache_and_install import show_cache, clear_cache
from install_uninstall_update_module import install, uninstall, update
from freeze_requirements import freeze, list_modules
from search_module import search_module
from init import init
import codecs
# imports all the required functions from the various files and modules


def help_message():
    '''
    Prints the help message for the cul CLI.

    Args:
        None
    
    Returns:
        None
    
    Raises:
        None
    '''
    help_text = """
    cul CLI - Command Line Interface for managing C/C++ libraries
    
    Commands:
        install library                            - Installs the specified C/C++ library.
        install library==version                   - Installs the specified version of the library.
        install library1 library2 library3 ...     - Installs multiple libraries. (Version is optional and can be specified for each library)
        uninstall library                          - Uninstalls the specified library.
        uninstall library1, library2, library3 ... - Uninstalls multiple libraries.
        update library                             - Updates the specified library to the latest version.
        update library1, library2, library3 ...    - Updates multiple libraries to the latest version.
        search library                             - Searches for the specified library and displays available versions.
        list                                       - Lists all installed libraries.
        freeze                                     - Outputs the installed libraries in requirements.txt format.
        help                                       - Shows the help message.
        cache clear                                - Clears the cache of the installed libraries.
        cache show                                 - Shows the cached modules along with their versions.
        init                                       - Initializes the project with a module_info.json file.
        init -y                                    - Initializes the project with a module_info.json file without asking for confirmation.

    MADE WITH ❤️ BY ATRI THAKAR
    """
    print(help_text)


def main():
    # Check if the user has provided a command
    if len(sys.argv) < 2:
        help_message()
        return

    command = sys.argv[1]

    if command == 'install':
        if len(sys.argv) < 3: # No library specified, print error message and help message
            print_in_red("Error: No library specified for installation.")
            help_message()
            return
        elif sys.argv[2] == '-r':  # Install from a requirements file
            if len(sys.argv) < 4:  # No requirements file specified, print error message and help message
                print_in_red("Error: No requirements file specified for installation.")
                help_message()
                return
            with codecs.open(sys.argv[3], 'r', encoding='ascii') as f:
                lines = f.readlines()
                for line in lines:
                    install(line.strip())
        else:  # Install individual libraries
            for i in range(2, len(sys.argv)):
                install(sys.argv[i])

    elif command == 'uninstall':
        if len(sys.argv) < 3: # No library specified, print error message and help message
            print_in_red("Error: No library specified for uninstallation.")
            help_message()
        else: # Uninstall individual libraries
            for i in range(2, len(sys.argv)):
                uninstall(sys.argv[i])

    elif command == 'update':
        if len(sys.argv) < 3: # No library specified, print error message and help message
            print_in_red("Error: No library specified for updating.")
            help_message()
        else: # Update individual libraries
            for i in range(2, len(sys.argv)):
                update(sys.argv[i])

    elif command == 'help': 
        help_message() # Print the help message

    elif command == 'freeze':
        freeze() # Print the installed libraries in requirements.txt format

    elif command == 'list':
        list_modules() # List all the installed libraries

    elif command == 'search':
        if len(sys.argv) < 3: # No library specified, print error message and help message
            print_in_red("Error: No library specified for searching.")
            help_message()
        else: # Search for the specified library
            search_module(sys.argv[2])

    elif command == 'cache':
        if len(sys.argv) < 3: # No command specified, print error message and help message
            print_in_red("Error: No command specified related to cache.")
            help_message()
        elif sys.argv[2] == 'clear': # Clear the cache
            clear_cache()
        elif sys.argv[2] == 'show': # List the cached modules along with their versions
            show_cache()

    elif command == 'init': # Initialize the cul CLI
        if len(sys.argv) > 2 and sys.argv[2] == '-y':
            init(True)
            return
        init(False)

    else: # Invalid command, print error message and help message
        print_in_red(f"Unknown command: {command}")
        help_message()


if __name__ == "__main__":
    main()
