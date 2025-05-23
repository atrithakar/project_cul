def install_help():
    help_text = """
    install module                                                - Installs the specified C/C++ module.
    install module==version                                       - Installs the specified version of the module.
    install module1, module2, module3 ...                         - Installs multiple modules. (Version is optional and can be specified for each module)
    install -r requirements.txt                                   - Installs the modules specified in the requirements.txt file.
    install module1, module2, module3 --use-reg "registry_url"    - Installs the specified module from the specified registry.
    install -r requirements.txt --use-reg "registry_url"          - Installs the modules specified in the requirements.txt file from the specified registry.
    """
    print(help_text)

def uninstall_help():
    help_text = """
    uninstall module                           - Uninstalls the specified module.
    uninstall module1, module2, module3 ...    - Uninstalls multiple modules.
    uninstall -r requirements.txt              - Uninstalls the modules specified in the requirements.txt file, will ignore the versions specified in the file.
    """
    print(help_text)

def update_help():
    help_text = """
    update module                                                    - Updates the specified module to the latest version (available in either server or cache, depending upon the situation).
    update module1, module2, module3 ...                             - Updates multiple modules to the latest version.
    update module1, module2, module3 ... --use-reg "registry_url"    - Updates multiple modules from the specified registry.
    update -r requirements.txt                                       - Updates the modules specified in the requirements.txt file, will ignore the versions specified in the file.
    update -r requirements.txt --use-reg "registry_url"              - Updates the modules specified in the requirements.txt file from the specified registry.
    """
    print(help_text)

def search_help():
    help_text = """
    search module                                     - Searches for the specified module and displays available versions.
    search module --use-reg "registry_url"            - Searches for the specified module from the specified registry and displays available versions.
    search --fuzzy module                             - Searches for the specified module using fuzzy search and displays the modules with similar names.
    search --fuzzy module --use-reg "registry_url"    - Searches for the specified module using fuzzy search from the specified registry and displays the modules with similar names.
    """
    print(help_text)

def list_help():
    help_text = """
    list                       - Lists all installed modules in human readable format.
    list > requirements.txt    - Lists all installed modules in human readable format and stores the output in a file.
    """
    print(help_text)

def freeze_help():
    help_text = """
    freeze                       - Lists all installed modules in machine readable format.
    freeze > requirements.txt    - Lists all installed modules in machine readable format and stores the output in a file.
    """
    print(help_text)

def cache_help():
    help_text = """
    cache clear    - Removes the stored cache data for the installed modules.
    cache show     - Shows the cached modules along with their versions.
    """
    print(help_text)

def init_help():
    help_text = """
    init       - Initializes the project with a module_info.json file.
    init -y    - Initializes the project with a module_info.json file without asking for confirmation.
    """
    print(help_text)

def help_help():
    help_text = """
    help            - Shows the help full message.
    help command    - Shows the help message for the specified command.
    """
    print(help_text)

def set_reg_help():
    help_text = """
    set-reg link    - Changes the registry link in the configuration file to the link inputted by the user.
    set-reg default - Resets the registry link to the default registry link.
    """
    print(help_text)


def help_message(func_help: str = None):
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
    cul CLI - Command Line Interface for managing C/C++ modules
    
    Commands:
        install module                                                - Installs the specified C/C++ module.
        install module==version                                       - Installs the specified version of the module.
        install module1, module2, module3 ...                         - Installs multiple modules. (Version is optional and can be specified for each module)
        install -r requirements.txt                                   - Installs the modules specified in the requirements.txt file.
        install module1, module2, module3 --use-reg "registry_url"    - Installs the specified module from the specified registry.
        install -r requirements.txt --use-reg "registry_url"          - Installs the modules specified in the requirements.txt file from the specified registry.

        uninstall module                                              - Uninstalls the specified module.
        uninstall module1, module2, module3 ...                       - Uninstalls multiple modules.
        uninstall -r requirements.txt                                 - Uninstalls the modules specified in the requirements.txt file, will ignore the versions specified in the file.

        update module                                                 - Updates the specified module to the latest version (available in either server or cache, depending upon the situation).
        update module1, module2, module3 ...                          - Updates multiple modules to the latest version.
        update module1, module2, module3 ... --use-reg "registry_url" - Updates multiple modules from the specified registry.
        update -r requirements.txt                                    - Updates the modules specified in the requirements.txt file, will ignore the versions specified in the file.
        update -r requirements.txt --use-reg "registry_url"           - Updates the modules specified in the requirements.txt file from the specified registry.
        
        search module                                                 - Searches for the specified module and displays available versions.
        search module --use-reg "registry_url"                        - Searches for the specified module from the specified registry and displays available versions.
        search --fuzzy module                                         - Searches for the specified module using fuzzy search and displays the modules with similar names.
        search --fuzzy module --use-reg "registry_url"                - Searches for the specified module using fuzzy search from the specified registry and displays the modules with similar names.
        
        list                                                          - Lists all installed modules in human readable format.
        list > requirements.txt                                       - Lists all installed modules in human readable format and stores the output in a file.
        
        freeze                                                        - Lists all installed modules in machine readable format.
        freeze > requirements.txt                                     - Lists all installed modules in machine readable format and stores the output in a file.
        
        help                                                          - Shows the help message.
        
        cache clear                                                   - Removes the stored cache data for the installed modules.
        cache show                                                    - Shows the cached modules along with their versions.
        
        init                                                          - Initializes the project with a module_info.json file.
        init -y                                                       - Initializes the project with a module_info.json file without asking for confirmation.

        help                                                          - Shows the help full message.
        help command                                                  - Shows the help message for the specified command.

        set-reg link                                                  - Changes the registry link in the configuration file to the link inputted by the user.
        set-reg default                                               - Resets the registry link to the default registry link.

    NOTE: To store the output of any command into a file, use the following syntax:
            cul <command> > <filename>.txt
          
    NOTE: The registry URL must be enclosed in double quotes or single quotes and must contain the protocol (http/https).

    NOTE: To display the help message for a specific command, use the following syntax:
            cul help <command>
            If the command contains a hyphen/s, replace it with underscore/s.

    MADE WITH ❤️ BY ATRI THAKAR
    """
    if func_help:   
        func_name = func_help + "_help"
        if func_name in globals():
            globals()[func_name]()
            return

        print(f"Help message for '{func_help}' not found.")

    print(help_text)