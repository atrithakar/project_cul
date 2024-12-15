# CUL

## What is CUL?

CUL is a command-line utility for the C/C++ programming language that simplifies the downloading and management of external modules (header files).  

Inspired by Python's pip, the goal of CUL is to provide an efficient and user-friendly way to manage project-specific header files, making them easier to download, update, and organize.

The modules are stored in a separate repository along with the code of the backend file server, which can be accessed here: [c_cpp_modules](https://github.com/atrithakar/cul_backend).

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
