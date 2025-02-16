import sys
from colorful_outputs import print_in_red
from cache_and_install import show_cache, clear_cache
from install_uninstall_module import install, uninstall
from update_module import update
from freeze_requirements import freeze, list_modules
from search_module import search_module
from init import init
from helper_functions import handle_req_file_ops
import codecs
import chardet
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

    match command:
        case 'install':
            if len(sys.argv) < 3:
                print_in_red("Error: No library specified for installation.")
                help_message()
                return
            if sys.argv[2] == '-r':
                if len(sys.argv) < 4:
                    print_in_red("Error: No requirements file specified for installation.")
                    help_message()
                    return
                handle_req_file_ops(sys.argv[3], install)
            else:
                for i in range(2, len(sys.argv)):
                    install(sys.argv[i])

        case 'uninstall':
            if len(sys.argv) < 3:
                print_in_red("Error: No library specified for uninstallation.")
                help_message()
                return
            if sys.argv[2] == '-r':
                if len(sys.argv) < 4:
                    print_in_red("Error: No requirements file specified for uninstallation.")
                    help_message()
                    return
                handle_req_file_ops(sys.argv[3], uninstall)
            else:
                for i in range(2, len(sys.argv)):
                    uninstall(sys.argv[i])

        case 'update':
            if len(sys.argv) < 3:
                print_in_red("Error: No library specified for updating.")
                help_message()
                return
            if sys.argv[2] == '-r':
                if len(sys.argv) < 4:
                    print_in_red("Error: No requirements file specified for updating.")
                    help_message()
                    return
                handle_req_file_ops(sys.argv[3], update)
            else:
                for i in range(2, len(sys.argv)):
                    update(sys.argv[i])

        case 'help':
            help_message()

        case 'freeze':
            freeze()

        case 'list':
            list_modules()

        case 'search':
            if len(sys.argv) < 3:
                print_in_red("Error: No library specified for searching.")
                help_message()
                return
            search_module(sys.argv[2])

        case 'cache':
            if len(sys.argv) < 3:
                print_in_red("Error: No command specified related to cache.")
                help_message()
                return
            match sys.argv[2]:
                case 'clear':
                    clear_cache()
                case 'show':
                    show_cache()
                case _:
                    print_in_red(f"Unknown cache command: {sys.argv[2]}")
                    help_message()

        case 'init':
            init(True if len(sys.argv) > 2 and sys.argv[2] == '-y' else False)

        case _:
            print_in_red(f"Unknown command: {command}")
            help_message()


if __name__ == "__main__":
    main()
