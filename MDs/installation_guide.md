# How to Install?

Note: This project was built in python 3.12, so it is recommended to use the same version for the best results.

1. Create a folder: [OPTIONAL]
    ```bash
    mkdir cul
    ```
2. Create a virtual environment (so that your global python configuration doesn't get messed up): [OPTIONAL]
    ```bash
    python -m venv cul_env
    ```
3. Activate the environment: [OPTIONAL]
    ```bash
    cul_env/Scripts/activate
    ```

4. Clone this repository:
    ```bash
    git clone https://github.com/atrithakar/project_cul
    ```
5. Install the requirements:
    ```bash
    pip install -r requirements.txt
    ```

6. Install the latest version of `pyinstaller`:
    ```bash
    pip install pyinstaller --upgrade
    ```

7. Compile the code using `pyinstaller`:
    ```bash
    pyinstaller --onefile cul.py
    ```

8. For windows, add `cul.exe` to your system's `PATH` and for linux copy `cul` to `/bin`

Note: It is recommended to create a directory named ```cul``` in a secure location where it is unlikely to be deleted accidentally. For Windows, this could be the ```C:``` drive, and for Linux, an appropriate location might be ```/opt``` or a directory under the user's home directory (e.g., ```~/cul```).