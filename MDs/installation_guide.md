# How to Install?

**Note**: This project was built in python 3.12, so it is recommended to use the same version for the best results.<br>
**Note**: Steps marked as **OPTIONAL** are recommended for a smoother, error-free installation. However, if you choose to follow them, you must complete all related **OPTIONAL** steps together. For instance, you can either skip steps 1 to 3 entirely or follow all of them.

Step 1: Create a folder: [OPTIONAL]<br>
```bash
mkdir cul
```
Step 2: Create a virtual environment (so that your global python configuration doesn't get messed up): [OPTIONAL]<br>
```bash
python -m venv cul_env
```
Step 3: Activate the environment: [OPTIONAL]<br>
```bash
cul_env/Scripts/activate
```

Step 4: Clone this repository:<br>
```bash
git clone https://github.com/atrithakar/project_cul
```
Step 5: Install the requirements:<br>
```bash
pip install -r requirements.txt
```

Step 6: Install the latest version of `pyinstaller`:<br>
```bash
pip install pyinstaller --upgrade
```

Step 7: Compile the code using `pyinstaller`:<br>
```bash
pyinstaller --onefile cul.py
```

Step 8: For windows, add `cul.exe` to your system's `PATH` and for linux copy `cul` to `/bin`

**Note**: It is recommended to create a directory named ```cul``` in a secure location where it is unlikely to be deleted accidentally. For Windows, this could be the ```C:``` drive, and for Linux, an appropriate location might be ```/opt``` or a directory under the user's home directory (e.g., ```~/cul```).