# CUL

## What is CUL?

CUL is a command-line utility for the C/C++ programming language that simplifies the downloading and management of external modules (header files).  

Inspired by Python's pip and NodeJS's npm, the goal of CUL is to provide an efficient and user-friendly way to manage project-specific header files, making them easier to download, update, and organize.

The modules are stored in a separate repository along with the code of the backend file server, which can be accessed here: [CUL Backend](https://github.com/atrithakar/cul_backend).

---
## Features:
- Provides minimalistic UI.
- Installs modules directly into project directory.
- Allows searching for the versions availabe, if any, before installing the module.
- Uses caching technique to install the module again in less amount of time without using the internet.
- Provides a way to list all the modules installed, both in human readable way and machine readable way, and store them into a .txt file.
- Allows downloading different versions of modules.
- Provides the way to initialize a project and maintain dependencies/requirements easily.
- Installs all the required modules by the current installing module automatically

---

## How to Install?

Note: This project was built in python 3.12, so it is recommended to use the same version for best results.

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

---

## How to Use?

### Installing a New Module:
```bash
cul install module_name
```

### Installing a Specific Version of a Module:
```bash
cul install module_name==version
```

### Installing Modules From a Dependency File:
```bash
cul install -r file_name.txt
```

### Uninstalling an Existing Module:
```bash
cul uninstall module_name
```

### Uninstalling Modules From a Dependency File:
```bash
cul uninstall -r file_name.txt
```
Note: This will ignore the versions specified and will uninstall based on the specified module name only. It also ignores the modules that are mentioned in the dependency file but have not been installed.

### Updating a Module:
```bash
cul update module_name
```

### Updating Modules From a Dependency File:
```bash
cul update -r file_name.txt
```
Note: Just like the uninstall command, this will also ignore the version of the modules specified in dependency file and will update the mentioned module/s to the latest version available on the server or in the cache if there's some error while contacting the server such as server down or internet issues. This command will also ignore the modules that are mentioned in the dependency file but have not been installed.

### Listing Installed Modules in Human Readable Format:
```bash
cul list
```

### Listing Installed Modules in Human Readable Format Into a Text File:
```bash
cul list > installed_modules.txt
```

### Listing Installed Modules in Machine Readable Format:
```bash
cul freeze
```

### Listing Installed Modules in Machine Readable Format Into a Text File:
```bash
cul freeze > requirements.txt
```

### Printing Help Message:
```bash
cul help
```
### Clearing Cache:
```bash
cul cache clear
```

### Displaying Cached Modules Along With The Versions of Each Module Cached:
```bash
cul cache show
```

### Initializing a Project:
```bash
cul init
```

### Initializing a Project Without Any Questions Asked:
```bash
cul init -y
```
Note: This will, as expected, not ask any questions while initializing a project but will fill the values with default values specified by the developer.

---

## How to Contribute?

CUL is an open-source project, and contributions from the community are highly welcome!  

If you have the skills and passion to improve this tool, feel free to contribute. All contributions will go through a thorough code review process before being approved.

### Steps to Contribute:
1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Commit your changes and create a pull request.
4. Wait for the code review and approval.

---

Thank you for contributing to CUL and making it better!

Feel free to share feedback or report issues in the [GitHub Issues](https://github.com/atrithakar/project_cul/issues) section. Let's make C/C++ library management hassle-free together!

---
## A little backstory:
During my early college days, I began learning Python after gaining experience with the C language. I often wondered why C didn't have a package management tool like Python's pip, which sparked an idea in me to create one. This project became my dream, motivated by my love for programming rather than the pursuit of fame or financial success.

At that time, I was unaware of existing tools like vcpkg and Conan that provide package management for C/C++. Instead of feeling discouraged by their existence, I found inspiration in them to improve my own tool, CUL. Initially, my plan was to implement basic functionalities such as installing, uninstalling, updating, and providing help.
However, as I worked on the project, my desire to enhance its capabilities grew.

I continue to develop CUL with the hope of making it a valuable resource for others in the C/C++ community. I recognize the many excellent tools available and aim to learn from them while striving to contribute positively to the ecosystem. This journey is about growth, learning, and sharing knowledge within the programming community.