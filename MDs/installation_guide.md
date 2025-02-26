# How to Install?

**Note**: This project was built in python 3.12, so it is recommended to use the same version for the best results.
**Note**: The steps with **OPTIONAL** written after them are recommended to follow if you want an error free installation.

Step 1. Create a folder: [OPTIONAL]
    ```bash
    mkdir cul
    ```
Step 2. Create a virtual environment (so that your global python configuration doesn't get messed up): [OPTIONAL]
    ```bash
    python -m venv cul_env
    ```
Step 3. Activate the environment: [OPTIONAL]
    ```bash
    cul_env/Scripts/activate
    ```

Step 4. Clone this repository:
    ```bash
    git clone https://github.com/atrithakar/project_cul
    ```
Step 5. Install the requirements:
    ```bash
    pip install -r requirements.txt
    ```

Step 6. Install the latest version of `pyinstaller`:
    ```bash
    pip install pyinstaller --upgrade
    ```

Step 7. Compile the code using `pyinstaller`:
    ```bash
    pyinstaller --onefile cul.py
    ```

Step 8. For windows, add `cul.exe` to your system's `PATH` and for linux copy `cul` to `/bin`

Note: It is recommended to create a directory named ```cul``` in a secure location where it is unlikely to be deleted accidentally. For Windows, this could be the ```C:``` drive, and for Linux, an appropriate location might be ```/opt``` or a directory under the user's home directory (e.g., ```~/cul```).