import urllib.request
import json
from common_variables import BASE_URL
from colorful_outputs import print_in_red, print_in_yellow

from rapidfuzz import process

def fuzzy_search_module(query, limit=5, threshold=50):
    """
    Performs fuzzy search on the given list of module names.

    Args:
        query (str): The search string entered by the user.
        limit (int): Maximum number of results to return.
        threshold (int): Minimum match score to consider a result.

    Returns:
        list: List of matching module names.

    Raises:
        None
    """

    module_names_url = f"{BASE_URL}/modules"

    req = urllib.request.Request(module_names_url)

    module_names = None
    with urllib.request.urlopen(req) as response:
        if response.status != 200:
            raise Exception(f"HTTP {response.status}: Unable to fetch module names.")

        module_names_data = response.read().decode()
        module_names = json.loads(module_names_data)

    results = process.extract(query, module_names, limit=limit, score_cutoff=threshold)
    return [match[0] for match in results]  # Extracting matched names

def search_module(module_name: str):
    '''
    Searches if the module is available on the server and prints the available versions along with the latest version.

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

        with urllib.request.urlopen(search_url) as response:
            if response.status != 200:
                raise urllib.error.HTTPError(search_url, response.status, f"Unable to fetch versions for {module_name}.", response.getheaders(), None)

            module_data = response.read().decode()

        module_info = json.loads(module_data)

        print(f"Module: {module_name}")

        available_versions = module_info.get("versions", [])
        latest_version = module_info.get("latest", "Unknown")
        latest_path = module_info.get("latest_path", "N/A")
        requirements = module_info.get("requires", {})

        if not available_versions:
            print_in_yellow("No versions available.")
            return

        print("\nAvailable versions:")
        for version_entry in available_versions:
            version = version_entry.get("version", "Unknown")
            path = version_entry.get("path", "N/A")
            print(f"  - {version}")

            # Print dependencies if they exist for this version
            if not (version in requirements and requirements[version]):
                continue
            print("    Requires:")
            for req in requirements[version]:
                print(f"    - {req}")
            print()

        print(f"Latest version: {latest_version}")

    except urllib.error.HTTPError as http_err:
        print_in_red(f"HTTP error: {http_err.code} {http_err.reason}")

    except urllib.error.URLError as url_err:
        print_in_red(f"URL error: {url_err.reason}")

    except json.JSONDecodeError:
        print_in_red("Failed to decode the JSON response. Please check the server response.")

    except KeyError as key_err:
        print_in_red(f"Key error: Missing key in JSON response: {key_err}")

    except Exception as e:
        print_in_red(f"Unexpected error: {e}")


if __name__ == "__main__":
    print(fuzzy_search_module("x"))  # Example Usage: Search for the "File Management" module