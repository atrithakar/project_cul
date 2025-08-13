import os
import json

def add_file(file_name: str) -> None:
    '''
    Adds the mentioned file to the module_info.json file so that the future `cul compile` command knows how many files to compile.
    If the file does not exist, it will create a new blank file with the given name.

    Args:
        file_name (str): The name of the file to be added.

    Returns:
        None

    Raises:
        FileNotFoundError: If module_info.json does not exist.
        json.JSONDecodeError: If module_info.json is not a valid JSON file.
        Exception: For any other unexpected errors.
    '''

    try:
        with open("module_info.json", "r") as f:
            module_info = json.load(f)

        if "files" not in module_info:
            module_info["files"] = []

        if file_name in module_info["files"]:
            print(f"{file_name} is already in the module_info.json file.")
            return
        
        module_info["files"].append(file_name)

        with open("module_info.json", "w") as f:
            json.dump(module_info, f, indent=4)


        if not os.path.exists(file_name):
            print(f"{file_name} does not exist. Creating a new file.")
            with open(file_name, "w") as f:
                f.write(f"// This is the {file_name} file.\n")

        print(f"{file_name} added successfully.")

    except FileNotFoundError:
        print("module_info.json not found. Please initialize the project first.")
        return
    except json.JSONDecodeError:
        print("Error decoding module_info.json. Please check the file format.")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return
    
def remove_file(file_name: str, delete_file: bool = False) -> None:
    '''
    Removes the mentioned file from the module_info.json file and optionally deletes the file from the filesystem.

    Args:
        file_name (str): The name of the file to be removed.
        delete_file (bool): If True, the file will be deleted from the filesystem else it will only be removed from the module_info.json file. Default is False.

    Returns:
        None

    Raises:
        FileNotFoundError: If module_info.json does not exist.
        json.JSONDecodeError: If module_info.json is not a valid JSON file.
        Exception: For any other unexpected errors.
    '''
    try:
        with open("module_info.json", "r") as f:
            module_info = json.load(f)

        if "files" not in module_info or file_name not in module_info["files"]:
            print(f"{file_name} is not in the module_info.json file.")
            return
        
        module_info["files"].remove(file_name)

        with open("module_info.json", "w") as f:
            json.dump(module_info, f, indent=4)

        print(f"{file_name} removed successfully from module_info.json.")
        
        if not delete_file:
            return
        
        if not os.path.exists(file_name):
            print(f"{file_name} does not exist.")
            return
        
        os.remove(file_name)
        print(f"{file_name} deleted successfully.")
              
    except FileNotFoundError:
        print("module_info.json not found. Please initialize the project first.")
        return
    except json.JSONDecodeError:
        print("Error decoding module_info.json. Please check the file format.")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return

if __name__ == "__main__":
    add_file("Hello2.c")
    add_file("Hello3.c")
    # add_file("Hello4.c")
    # add_file("Hello5.c")
    # add_file("Hello6.c")
    # add_file("Hello7.c")
    # add_file("Hello8.c")

    # remove_file("Hello2.c")
    # remove_file("Hello3.c", True)

