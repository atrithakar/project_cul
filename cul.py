import sys
from colorful_outputs import print_in_red
from cache_and_install import *
from install_uninstall_update_module import *
from freeze_requirements import *
from search_module import *
from init import init

def help_message():
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

    """
    print(help_text)


def main():
    
    if len(sys.argv) < 2:
        help_message()
        return

    command = sys.argv[1]

    if command == 'install':
        if(sys.argv[2]=='-r'):
            with open(sys.argv[3], 'r') as f:
                for line in f:
                    install(line.strip())
        return
        if len(sys.argv) < 3:
            print_in_red("Error: No library specified for installation.")
            help_message()
        else:
            for i in range(2, len(sys.argv)):
                # print(sys.argv[i])
                # print("Installing...")
                install(sys.argv[i])
    elif command == 'uninstall':
        if len(sys.argv) < 3:
            print_in_red("Error: No library specified for uninstallation.")
            help_message()
        else:
            for i in range(2, len(sys.argv)):
                uninstall(sys.argv[i])
    elif command == 'update':
        if len(sys.argv) < 3:
            print_in_red("Error: No library specified for updating.")
            help_message()
        else:
            for i in range(2, len(sys.argv)):
                update(sys.argv[i])
    elif command == 'help':
        help_message()
    elif command == 'freeze':
        freeze()
    elif command == 'list':
        list_modules()
    elif command == 'search':
        if len(sys.argv) < 3:
            print_in_red("Error: No library specified for searching.")
            help_message()
        else:
            search_module(sys.argv[2])
    elif command == 'cache':
        if len(sys.argv) < 3:
            print_in_red("Error: No command specified related to cache.")
            help_message()
        elif sys.argv[2] == 'clear':
            clear_cache()
    elif command == 'init':
        init()
    else:
        print_in_red(f"Unknown command: {command}")
        help_message()

if __name__ == "__main__":
    main()
