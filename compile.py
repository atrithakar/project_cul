import os
import json
import re

'''
Currently focussing on:
- header files with .h file extension only.
- gcc compiler.
- c files with .c file extension only.
- Windows OS only.

- will expand later once this stabilizes.

currently in development, code will be cleaned soon and will be made more readable and documented.
'''

def parse_include_line(line: str) -> tuple[str, str, str]:
    start = line.find('"')
    end = line.rfind('"')
    if start >= end:
        raise ValueError("Invalid include line")
    
    full_path = line[start + 1:end]

    parts = full_path.rsplit('/', 1)
    file_name = parts[1] if len(parts) > 1 else parts[0]

    include_path = parts[0]
    if include_path.endswith('/include'):
        include_path = include_path[: -len('/include')]

    if '.' in file_name:
        module_name, module_ext = file_name.rsplit('.', 1)
        module_ext = '.' + module_ext
    else:
        module_name, module_ext = file_name, ''

    return include_path, module_name, module_ext



def extract_module_from_line(line: str, valid_header_exts: list[str]) -> tuple[str, str]:
    
    include_path, module_name, module_ext = parse_include_line(line)
    
    if not module_name:
        raise ValueError("Module name cannot be empty.")
    
    if module_ext not in valid_header_exts:
        raise ValueError(f"Invalid module file extension. Expected one of: {', '.join(valid_header_exts)}")
    

    return module_name, include_path

def compile(file_path: str):

    if not os.path.exists(file_path):
        print(f"The file {file_path} does not exist.")
        return
    
    valid_file_exts = ['.c'] # will add more later
    valid_header_exts = ['.h'] # will add more later
    file_name = os.path.basename(file_path)
    file_ext = os.path.splitext(file_name)[1]

    pattern_compile = re.compile(r'//\s*@cul\.compile')
    pattern_main_start = re.compile(r'//\s*@cul\.mainStart')

    if file_ext not in valid_file_exts:
        print(f"The file must be a C source file with one of the following extensions: {', '.join(valid_file_exts)}")
        return

    compile_command = f"gcc {file_name} -o {os.path.splitext(file_name)[0]} "

    try:
        modules = {}
        with open(file_path, 'r') as file:
            for line in file:
        
                if pattern_main_start.search(line):
                    # print("Main start found, breaking out of the loop because no imports are allowed after this point.")
                    break
                
                if not pattern_compile.search(line):
                    continue

                line2 = file.readline().strip()
                module_name, include_path = extract_module_from_line(line2, valid_header_exts)

                modules[module_name] = include_path

        for module, include_path in modules.items():
            compile_command += f"-I{include_path}/include/ "
            compile_command += f"-L{include_path}/bin/ "
            compile_command += f"-l{module} "
        
        return compile_command
    
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def compile_files():
    try:
        with open("module_info.json", "r") as f:
            data = json.load(f)
            files = data.get("files", [])
    except FileNotFoundError:
        print("module_info.json file not found.")
        return
    except json.JSONDecodeError:
        print("Error decoding JSON from module_info.json.")
        return
    except Exception as e:
        print(f"Unexpected error: {e}")
        return

    if not files:
        print("No files to compile.")
        return
    
    for file in files:
        print(compile(file))

        
if __name__ == '__main__':
    # print(compile("C:/work_of_atri/test/example.c")) 
    # compile_files() 
    print(compile("example.c"))             

