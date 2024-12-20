import urllib.request
import json
from common_variables import BASE_URL
from colorful_outputs import print_in_red, print_in_yellow


def search_module(module_name):
    try:
        search_url = f"{BASE_URL}/versions/{module_name}"

        with urllib.request.urlopen(search_url) as response:
            if response.status != 200:
                raise urllib.error.HTTPError(search_url, response.status, f"Unable to fetch versions for {module_name}.", response.getheaders(), None)
            
            module_data = response.read().decode()
            module_info = json.loads(module_data)
            print("Module name: ", module_name)
            available_versions = module_info.get("versions", [])
            latest_version = module_info.get("latest", "unknown")
            if available_versions:
                print("Available versions:")
                for version in available_versions:
                    print(f"  - {version.get('version')}")
                print(f"Latest version: {latest_version}")
            else:
                print_in_yellow("No versions available.")
            


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