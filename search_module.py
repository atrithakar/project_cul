import urllib.request
import json
from common_variables import BASE_URL
from colorful_outputs import print_in_red, print_in_yellow
from rapidfuzz import process

def fuzzy_search_module(query: str, limit: int = 5, threshold: int = 50, called_by_user: bool = False):
    """
    Performs fuzzy search on the given list of module names.

    Args:
        query (str): The search string entered by the user.
        limit (int): Maximum number of results to return.
        threshold (int): Minimum match score to consider a result.

    Returns:
        list: List of matching module names.

    Raises:
        HTTPError: If the server returns an unsuccessful status code.
        URLError: If the URL is invalid.
        JSONDecodeError: If the JSON decoding fails.
        Exception: If any unexpected error occurs.
    """

    module_names_url = f"{BASE_URL}/modules"
    module_names = None

    try:
        req = urllib.request.Request(module_names_url)
        with urllib.request.urlopen(req) as response:
            if response.status != 200:
                raise Exception(f"HTTP {response.status}: Unable to fetch module names.")

            module_names_data = response.read().decode()
            module_names = json.loads(module_names_data)

        results = process.extract(query, module_names, limit=limit, score_cutoff=threshold)
        if called_by_user:
            print(f"Search results for '{query}':")
            for match in results:
                print(f"  - {match[0]}")
            
        return [match[0] for match in results]  # Extracting matched names
    except urllib.error.HTTPError as e:
        print_in_red(f"HTTP Error: {e.code} {e.reason}")
    except urllib.error.URLError as e:
        print_in_red(f"URL Error: {e.reason}")
    except json.JSONDecodeError:
        print_in_red("Failed to decode the JSON response. Please check the server response.")
    except Exception as e:
        print_in_red(f"Unexpected Error: {e}")

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

        print(f"\nModule: {module_name}")
        print(f"Author: {module_info.get('author', 'Unknown')}")
        print(f"Description: {module_info.get('description', 'No description available.')}")
        print(f"License: {module_info.get('license', 'Unknown')}\n")

        all_versions = module_info.get('all_versions', {})
        versions = all_versions.get('versions', [])
        latest_version = all_versions.get('latest', 'Unknown')
        requires = all_versions.get('requires', {})

        if not versions:
            print_in_yellow("No versions available.")
            return

        print("Available versions:")
        for version_entry in versions:
            version = version_entry.get("version", "Unknown")
            print(f"  - {version}")

            if not requires.get(version):
                continue

            print("    Requires:")
            for req in requires[version]:
                print(f"    - {req}")

        print(f"\nLatest version: {latest_version}")

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
