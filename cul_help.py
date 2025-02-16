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
    cul CLI - Command Line Interface for managing C/C++ modules
    
    Commands:
        install module                             - Installs the specified C/C++ module.
        install module==version                    - Installs the specified version of the module.
        install module1 module2 module3 ...        - Installs multiple modules. (Version is optional and can be specified for each module)
        uninstall module                           - Uninstalls the specified module.
        uninstall module1, module2, module3 ...    - Uninstalls multiple modules.
        update module                              - Updates the specified module to the latest version (available in either server or cache, depending upon the situation).
        update module1, module2, module3 ...       - Updates multiple modules to the latest version.
        search module                              - Searches for the specified module and displays available versions.
        list                                       - Lists all installed modules in human readable format.
        freeze                                     - Lists all installed modules in machine readable format.
        help                                       - Shows the help message.
        cache clear                                - Removes the stored cache data for the installed modules.
        cache show                                 - Shows the cached modules along with their versions.
        init                                       - Initializes the project with a module_info.json file.
        init -y                                    - Initializes the project with a module_info.json file without asking for confirmation.

    NOTE: To store the output of any command into a file, use the following syntax:
        cul <command> > <filename>.txt

    MADE WITH ❤️ BY ATRI THAKAR
    """
    print(help_text)