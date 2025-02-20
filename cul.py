import sys
from colorful_outputs import print_in_red
from cache_and_install import show_cache, clear_cache
from install_uninstall_module import install, uninstall
from update_module import update
from freeze_requirements import freeze, list_modules
from search_module import search_module, fuzzy_search_module
from init import init
from helper_functions import handle_req_file_ops
from cul_help import help_message
import codecs
import chardet

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

            registry = None
            module_end = len(sys.argv)

            if '--use-reg' in sys.argv:
                reg_index = sys.argv.index('--use-reg')
                if reg_index + 1 >= len(sys.argv):
                    print_in_red("Error: No registry link was provided")
                    help_message()
                    return
                
                registry = sys.argv[reg_index + 1]
                module_end = reg_index

            if sys.argv[2] == '-r':
                if len(sys.argv) < 4:
                    print_in_red("Error: No requirements file specified for installation.")
                    help_message()
                    return
                handle_req_file_ops(sys.argv[3], install, registry)
            else:
                for i in range(2, module_end):
                    install(sys.argv[i], registry)

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

            registry = None
            module_end = len(sys.argv)

            if '--use-reg' in sys.argv:
                reg_index = sys.argv.index('--use-reg')
                if reg_index + 1 >= len(sys.argv):
                    print_in_red("Error: No registry link was provided")
                    help_message()
                    return
                
                registry = sys.argv[reg_index + 1]
                module_end = reg_index

            if sys.argv[2] == '-r':
                if len(sys.argv) < 4:
                    print_in_red("Error: No requirements file specified for installation.")
                    help_message()
                    return
                handle_req_file_ops(sys.argv[3], update, registry)
            else:
                for i in range(2, module_end):
                    update(sys.argv[i], registry)

        case 'help':
            help_message()

        case 'freeze':
            freeze()

        case 'list':
            list_modules()

        case 'search':
            if sys.argv[-1] == "--use-reg":
                print_in_red("Error: No registry link was provided")
                help_message()
                return

            registry = ''
            if sys.argv[-2] == '--use-reg':
                registry = sys.argv[-1]

            if sys.argv[2] == '--fuzzy':
                if len(sys.argv) < 4:
                    print_in_red("Error: No library specified for searching.")
                    help_message()
                    return
                fuzzy_search_module(query=sys.argv[3], called_by_user=True, registry=registry)
                return
            
            if len(sys.argv) < 3:
                print_in_red("Error: No library specified for searching.")
                help_message()
                return
            search_module(sys.argv[2], registry)

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
