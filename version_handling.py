import json
from colorful_outputs import print_in_red
def increment_patch():
    
    try:
        with open("module_info.json", "r") as f:
            module_info = json.load(f)

        version_parts = module_info["version"].split(".")
        if len(version_parts) != 3:
            raise ValueError("Version must be in the format 'major.minor.patch'")
    
        version_parts[2] = str(int(version_parts[2]) + 1)
        new_version = ".".join(version_parts)
        module_info["version"] = new_version

        with open("module_info.json", "w") as f:
            json.dump(module_info, f, indent=4)
    except FileNotFoundError:
        print_in_red("Error: 'module_info.json' file not found.")
    except json.JSONDecodeError:
        print_in_red("Error: Failed to decode JSON from 'module_info.json'.")
    except ValueError as ve:
        print_in_red(f"Error: {ve}")
    except Exception as e:
        print_in_red(f"An unexpected error occurred: {e}")

def increment_minor():
    try:
        with open("module_info.json", "r") as f:
            module_info = json.load(f)

        version_parts = module_info["version"].split(".")
        if len(version_parts) != 3:
            raise ValueError("Version must be in the format 'major.minor.patch'")
    
        version_parts[1] = str(int(version_parts[1]) + 1)
        version_parts[2] = "0"
        new_version = ".".join(version_parts)
        module_info["version"] = new_version

        with open("module_info.json", "w") as f:
            json.dump(module_info, f, indent=4)
    except FileNotFoundError:
        print_in_red("Error: 'module_info.json' file not found.")
    except json.JSONDecodeError:
        print_in_red("Error: Failed to decode JSON from 'module_info.json'.")
    except ValueError as ve:
        print_in_red(f"Error: {ve}")
    except Exception as e:
        print_in_red(f"An unexpected error occurred: {e}")

def increment_major():
    try:
        with open("module_info.json", "r") as f:
            module_info = json.load(f)

        version_parts = module_info["version"].split(".")
        if len(version_parts) != 3:
            raise ValueError("Version must be in the format 'major.minor.patch'")
    
        version_parts[0] = str(int(version_parts[0]) + 1)
        version_parts[1] = "0"
        version_parts[2] = "0"
        new_version = ".".join(version_parts)
        module_info["version"] = new_version

        with open("module_info.json", "w") as f:
            json.dump(module_info, f, indent=4)
    except FileNotFoundError:
        print_in_red("Error: 'module_info.json' file not found.")
    except json.JSONDecodeError:
        print_in_red("Error: Failed to decode JSON from 'module_info.json'.")
    except ValueError as ve:
        print_in_red(f"Error: {ve}")
    except Exception as e:
        print_in_red(f"An unexpected error occurred: {e}")
