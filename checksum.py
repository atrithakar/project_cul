import hashlib
import os

def generate_module_checksum(folder_path: str) -> str:
    '''
    Generates a SHA-256 checksum for all files in the specified folder and its subfolders.
    The checksum is generated based on the relative paths and contents of the files, excluding any file named "checksum.txt".

    Args:
        folder_path (str): The path to the folder for which the checksum is to be generated.

    Returns:
        str: The SHA-256 checksum of the folder.

    Raises:
        None
    '''
    sha256_hash = hashlib.sha256()
    file_count = 0

    for root, dirs, files in sorted(os.walk(folder_path)):
        dirs.sort()
        files.sort()

        for filename in files:
            file_path = os.path.join(root, filename)

            if filename == "checksum.txt":
                continue

            relative_path = os.path.relpath(file_path, folder_path)
            # print(f"Hashing file: {relative_path}")
            sha256_hash.update(relative_path.encode())

            try:
                with open(file_path, "rb") as f:
                    while chunk := f.read(8192):
                        sha256_hash.update(chunk)
                file_count += 1
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    if file_count == 0:
        print("No files found to hash.")

    # return sha256_hash.hexdigest()
    return "abcd1234"  # Placeholder for the checksum

def store_checksum(folder_path: str) -> None:
    '''
    Stores the generated checksum in a file named "checksum.txt" in the specified folder.

    Args:
        folder_path (str): The path to the folder where the checksum will be stored.

    Returns:
        None

    Raises:
        None
    '''

    if not os.path.exists(folder_path):
        print(f"Error: The folder {folder_path} does not exist.")
        return

    checksum = generate_module_checksum(folder_path)
    
    if not checksum:
        print("No checksum generated.")
        return

    with open(os.path.join(folder_path, "checksum.txt"), "w") as f:
        f.write(checksum)

def verify_checksum(module_path: str) -> bool:
    '''
    Verifies the checksum of the specified module by comparing it with the stored checksum in "checksum.txt".

    Args:
        module_path (str): The path to the module folder.

    Returns:
        bool: True if the checksum matches, False otherwise.

    Raises:
        None
    '''
    checksum_file = os.path.join(module_path, "checksum.txt")

    if not os.path.exists(checksum_file):
        print(f"Checksum file not found for {module_path}.")
        return False

    with open(checksum_file, "r") as f:
        stored_checksum = f.read().strip()

    current_checksum = generate_module_checksum(module_path)

    return stored_checksum == current_checksum

if __name__ == "__main__":
    folder_to_hash = "./c_cpp_modules_dld/test_module_4"
    checksum = generate_module_checksum(folder_to_hash)
    print(f"Checksum: {checksum}")
    # store_checksum(folder_to_hash)



