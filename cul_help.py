import os

HELP_MESSAGES = {
    "install": """
    install module                                                - Installs the specified C/C++ module.
    install module==version                                       - Installs the specified version of the module.
    install module1, module2, module3 ...                         - Installs multiple modules. (Version is optional and can be specified for each module)
    install -r requirements.txt                                   - Installs the modules specified in the requirements.txt file.
    install module1, module2, module3 --use-reg "registry_url"    - Installs the specified module from the specified registry.
    install -r requirements.txt --use-reg "registry_url"          - Installs the modules specified in the requirements.txt file from the specified registry.
    """,

    "uninstall": """
    uninstall module                           - Uninstalls the specified module.
    uninstall module1, module2, module3 ...    - Uninstalls multiple modules.
    uninstall -r requirements.txt              - Uninstalls the modules specified in the requirements.txt file, will ignore the versions specified in the file.
    """,

    "update": """
    update module                                                    - Updates the specified module to the latest version (available in either server or cache, depending upon the situation).
    update module1, module2, module3 ...                             - Updates multiple modules to the latest version.
    update module1, module2, module3 ... --use-reg "registry_url"    - Updates multiple modules from the specified registry.
    update -r requirements.txt                                       - Updates the modules specified in the requirements.txt file, will ignore the versions specified in the file.
    update -r requirements.txt --use-reg "registry_url"              - Updates the modules specified in the requirements.txt file from the specified registry.
    """,

    "search": """
    search module                                     - Searches for the specified module and displays available versions.
    search module --use-reg "registry_url"            - Searches for the specified module from the specified registry and displays available versions.
    search --fuzzy module                             - Searches for the specified module using fuzzy search and displays the modules with similar names.
    search --fuzzy module --use-reg "registry_url"    - Searches for the specified module using fuzzy search from the specified registry and displays the modules with similar names.
    """,

    "list": """
    list                       - Lists all installed modules in human readable format.
    list > requirements.txt    - Lists all installed modules in human readable format and stores the output in a file.
    """,

    "freeze": """
    freeze                       - Lists all installed modules in machine readable format.
    freeze > requirements.txt    - Lists all installed modules in machine readable format and stores the output in a file.
    """,

    "cache": """
    cache clear    - Removes the stored cache data for the installed modules.
    cache show     - Shows the cached modules along with their versions.
    """,

    "init": """
    init       - Initializes the project with a module_info.json file.
    init -y    - Initializes the project with a module_info.json file without asking for confirmation.
    """,

    "help": """
    help            - Shows the general help message.
    help command    - Shows the help message for the specified command.
    """,

    "set_reg": """
    set-reg link    - Changes the registry link in the configuration file to the link inputted by the user.
    set-reg default - Resets the registry link to the default registry link.
    """,

    "new": """
    new file_name    - Adds the specified file in the module_info.json file and creates a new file with the specified name if it does not exist.
    """,

    "remove": """
    remove file_name             - Removes the specified file from the module_info.json file.
    remove file_name --delete    - Removes the specified file from the module_info.json file and deletes the file from the filesystem.
    """,

    "compile": """
    compile - Compiles the files specified in the module_info.json file while automatically detecting the modules to be included based on the `@cul.compile` comments in the files and handles the compiler flags accordingly.
    """,

    "version" : """
    version patch   - Increments the patch version in module_info.json.
    version minor   - Increments the minor version in module_info.json and resets the patch version to 0.
    version major   - Increments the major version in module_info.json and resets the minor and patch versions to 0.
    """
}

GENERAL_HELP = f"""
cul CLI - Command Line Interface for managing C/C++ modules

Commands:
{os.linesep.join(f"  {cmd}" for cmd in HELP_MESSAGES.keys())}

NOTE: To display help for a specific command:
    cul help <command>
    (replace hyphen with underscore if present)

NOTE: To store the output of any command into a file, use:
    cul <command> > <filename>.txt

MADE WITH ❤️ BY ATRI THAKAR
"""

def help_message(command: str = None):
    if command:
        key = command.replace("-", "_")  # normalize
        if key in HELP_MESSAGES:
            print(HELP_MESSAGES[key])
            return
        else:
            print(f"Help message for '{command}' not found.")
            return
    
    print(GENERAL_HELP)
