import os
import json
from colorful_outputs import print_in_green, print_in_red, print_in_yellow

def init(all_yes: bool = False):
    '''
    Initializes the project by creating a module_info.json file based on the user's input.
    The user will be prompted to enter the name, version, description, author, license, keywords, entry point, test command, repository type, and repository URL.

    Args:
        None

    Returns:
        None, but creates a module_info.json file in the current directory.

    Raises:
        None

    '''
    if all_yes:
        name = os.getcwd().split("\\")[-1]
        version = "1.0.0"
        description = ""
        author = ""
        license = "MIT"
        keywords = []
        entry_point = "main.c"
        test_command = "None"
        repo_type = "git"
        repo_url = ""
    else:
        name = input(f"Enter the name of the project: ({os.getcwd().split("\\")[-1]}) ")
        if name == "":
            name = os.getcwd().split("\\")[-1]
        version = input("Enter the version of the project: (1.0.0) ")
        if version == "":
            version = "1.0.0"
        description = input("Enter the description of the project: ")
        author = input("Enter the author of the project: ")
        license = input("Enter the license of the project: (MIT) ")
        if license == "":
            license = "MIT"
        keywords = input("Enter the keywords for the project: (separated by commas) ")
        keywords = [keyword.strip() for keyword in keywords.split(",")]
        entry_point = input("Enter the entry point of the project: (main.py) ")
        if entry_point == "":
            entry_point = "main.c"
        test_command = input("Enter the test command for the project:")
        if test_command == "":
            test_command = "None"
        repo_type = input("Enter the repository type for the project: (git) ")
        if repo_type == "":
            repo_type = "git"
        repo_url = input("Enter the repository URL for the project: ")

    data = {
        "name": name,
        "version": version,
        "description": description,
        "author": author,
        "license": license,
        "keywords": keywords,
        "main": entry_point,
        "scripts": {
            "test": test_command
        },
        "repository": {
            "type": repo_type,
            "url": repo_url
        },
        "requires" : [

        ]
    }

    with open("module_info.json", "w") as f:
        json.dump(data, f, indent=4)
    print_in_green("Project initialized successfully.")


def add_requirements(module_name: str, version: str):
    '''
    Adds the module and its version to the requirements in the module_info.json file.

    Args:
        module_name (str): The name of the module.
        version (str): The version of the module.
    
    Returns:
        None, but adds the module and its version to the requirements in the module_info.json file.
    
    Raises:
        Unexpected error if there is an error adding the requirements.
    '''
    try:
        with open("module_info.json", "r") as f:
            data = json.load(f)
        
        currently_installed = data.get("requires", [])
        # print(currently_installed)
        for req in currently_installed:
            if module_name == req.split("==")[0]:
                data["requires"].remove(req)
                print(f"Removed the existing version of the module {module_name} v{req.split('==')[1]}")

        data["requires"].append(f"{module_name}=={version}")
        with open("module_info.json", "w") as f:
            json.dump(data, f, indent=4)
        print_in_green(f"Added '{module_name}=={version}' to the requirements.")
    except FileNotFoundError as e:
        # print_in_yellow("Warning: Project not initialized. Please run 'cul init' to initialize the project.")
        pass
        '''
        I had to do like this as the warning was kind of annoying from the user's perspective.
        If I remove this FileNotFoundError exception, then the code will show "Error adding requirements: {e}".
        So I had to keep this FileNotFoundError exception and write pass in the except block.
        This will remain as it is until I find a better way to handle this.
        '''
    except Exception as e:
        print_in_red(f"Error adding requirements: {e}")

def remove_requirements(module_name: str):
    '''
    Removes the module from the requirements in the module_info.json file.

    Args:
        module_name (str): The name of the module.

    Returns:
        None, but removes the module from the requirements in the module_info.json file.

    Raises:
        Unexpected error if there is an error removing the requirements.
    '''
    try:
        with open("module_info.json", "r") as f:
            data = json.load(f)

        original_length = len(data.get("requires", []))

        data["requires"] = [
            req for req in data["requires"] if req.split("==")[0] != module_name
        ]
        if len(data["requires"]) >= original_length:
            print_in_yellow(f"Module '{module_name}' not found in the requirements.")
            return
        with open("module_info.json", "w") as f:
            json.dump(data, f, indent=4)
        print_in_green(f"Removed '{module_name}' from the requirements.")
        
    except FileNotFoundError:
        pass
        '''
        I had to do like this as the warning was kind of annoying from the user's perspective.
        If I remove this FileNotFoundError exception, then the code will show "Error removing requirements: {e}".
        So I had to keep this FileNotFoundError exception and write pass in the except block.
        This will remain as it is until I find a better way to handle this.
        '''
    except json.JSONDecodeError as e:
        print_in_red("Error reading JSON file. It may be corrupted.")
    except Exception as e:
        print_in_red(f"Error removing requirements: {e}")
