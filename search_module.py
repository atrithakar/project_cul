import urllib.request
import json
from common_variables import BASE_URL
from colorful_outputs import print_in_red, print_in_yellow
from thefuzz import process

# will implement fuzzy search later, cuz for that i'll have to develop a new feature.


def search_module(module_name: str):
    '''
    Searches if the module is available on the server and prints the available versions along with the latest version

    Args:
        module_name (str): The name of the module to search
    
    Returns:
        None

    Raises:
        HTTPError: If the server returns an unsuccessful status code
        URLError: If the URL is invalid
        JSONDecodeError: If the JSON decoding fails
        KeyError: If the JSON response is missing keys
        Exception: If any unexpected error occurs
    '''
    try:
        search_url = f"{BASE_URL}/versions/{module_name}"

        module_data = None
        with urllib.request.urlopen(search_url) as response:
            if response.status != 200:
                raise urllib.error.HTTPError(search_url, response.status, f"Unable to fetch versions for {module_name}.", response.getheaders(), None)
            
            module_data = response.read().decode()

        module_info = json.loads(module_data)
        print("Module name:", module_name)
        available_versions = module_info.get("requires", [])
        latest_version = module_info.get("latest", "unknown")

        if not available_versions:
            print_in_yellow("No versions available.")
            return

        print("Available versions:")
        for version, requirements in available_versions.items():
            print(f"  - {version}")
            if not requirements:
                print()
                continue
            print("    Requires:")
            for req in requirements:
                print(f"    - {req}")
            print()

        print("Latest version:", latest_version)

    except urllib.error.HTTPError as http_err:
        # Detailed HTTP error message including the status code and reason
        print_in_red(f"HTTP error: {http_err.code} {http_err.reason}")
    
    except urllib.error.URLError as url_err:
        # Error handling for general URL errors (e.g., network issues, invalid URL)
        print_in_red(f"URL error: {url_err.reason}")
    
    except json.JSONDecodeError:
        # Error handling if JSON decoding fails
        print_in_red("Failed to decode the JSON response. Please check the server response.")
    
    except KeyError as key_err:
        # Error handling for missing keys in the JSON response
        print_in_red(f"Key error: {key_err}")
    
    except Exception as e:
        # General exception handling for unexpected errors
        print_in_red(f"Unexpected error: {e}")