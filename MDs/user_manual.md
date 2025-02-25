# How to Use?

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

### Installing Module From a Different Registry:
```bash
cul install module_name --use-reg "registry_url"
```
NOTE: registry_url must be enclosed in double and single quotes and must contain the protocol (http/https).

### Uninstalling an Existing Module:
```bash
cul uninstall module_name
```

### Uninstalling Modules From a Dependency File:
```bash
cul uninstall -r file_name.txt
```
Note: This will ignore the versions specified and will uninstall based on the specified module name only. It also ignores the modules that are mentioned in the dependency file but have not been installed.

### Searching For a Module:
```bash
cul search module_name
```
Note: This will search for `module_name` on the server and returns ONLY if the exact match is found, else gives a 404 error.

### Searching For a Module Without Knowing the Exact Name:
```bash
cul search --fuzzy module_name
```
Note: Finds and lists all modules with names similar to `module_name`.

### Updating a Module:
```bash
cul update module_name
```

### Updating Modules From a Dependency File:
```bash
cul update -r file_name.txt
```
Note: Just like the uninstall command, this will also ignore the version of the modules specified in dependency file and will update the mentioned module/s to the latest version available on the server or in the cache if there's some error while contacting the server such as server down or internet issues. This command will also ignore the modules that are mentioned in the dependency file but have not been installed.

### Updating Module From Different Registry:
```bash
cul update module_name --use-reg "registry_url"
```
NOTE: registry_url must be enclosed in double and single quotes and must contain the protocol (http/https).

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

### Printing Help Message For Specific Command:
```bash
cul help command_name
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