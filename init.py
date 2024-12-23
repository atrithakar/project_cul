import os
import json
from colorful_outputs import print_in_green, print_in_red, print_in_yellow

def init():
    name = input(f"Enter the name of the project: ({os.getcwd().split("/")[-1]}) ")
    if name == "":
        name = os.getcwd().split("/")[-1]
    version = input("Enter the version of the project: (1.0.0) ")
    if version == "":
        version = "1.0.0"
    description = input("Enter the description of the project: ")
    author = input("Enter the author of the project: ")
    license = input("Enter the license of the project: (MIT) ")
    if license == "":
        license = "MIT"
    keywords = input("Enter the keywords for the project: (separated by commas) ")
    keywords = keywords.split(",")
    entry_point = input("Enter the entry point of the project: (main.py) ")
    if entry_point == "":
        entry_point = "main.py"
    test_command = input("Enter the test command for the project: (python -m unittest discover) ")
    if test_command == "":
        test_command = "python -m unittest discover"
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


def add_requirements(module_name, version):
    try:
        with open("module_info.json", "r") as f:
            data = json.load(f)
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