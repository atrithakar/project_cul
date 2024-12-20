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

---

## How to Install?

### For Windows:

1. Open your terminal.
2. Clone the repository:
   ```bash
   git clone https://github.com/atrithakar/project_cul
   ```
3. Move the `cul.exe` file to `C:/Windows/System32`:
   ```bash
   move cul.exe C:/Windows/System32
   ```

### For Linux:

1. Open your terminal.
2. Clone the repository:
   ```bash
   git clone https://github.com/atrithakar/project_cul
   ```
3. Move the `cul` file to `/bin`:
   ```bash
   mv /path/to/cul /bin
   ```

You can then remove the residual files if you wish.

---

## How to Build? (If You Want to Build It Youself)

1. Install `pyinstaller`:
    ```bash
    pip install pyinstaller
    ```

2. Compile the code using `pyinstaller`:
    ```bash
    pyinstaller --onefile cul.py
    ```

---

## How to Use?

### Installing a New Header File
```bash
cul install header_file_name
```

### Installing a Specific Version of a Header File
```bash
cul install header_file_name==version
```

### Uninstalling an Existing Header File
```bash
cul uninstall header_file_name
```

### Updating a Header File
```bash
cul update header_file_name
```

### Listing installed modules
```bash
cul list
```

### Listing installed modules and storing them into a text file
```bash
cul list > installed_modules.txt
```

### Listing installed requirements
```bash
cul freeze
```

### Listing installed requirements and storing them into a text file
```bash
cul freeze > requirements.txt
```

### Getting Help
```bash
cul help
```


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