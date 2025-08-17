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
'''

# currently in development, code will be cleaned soon and will be made more readable and documented.

def extract_module_from_line(line: str, valid_header_exts: list[str]) -> str:
    start = line.index('"')
    end = line.rindex('"')
    if start >= end:
        raise ValueError("Invalid import")
    
    module_name = os.path.basename(line[start + 1:end])

    if not module_name:
        raise ValueError("Module name cannot be empty.")
    
    module_ext = os.path.splitext(module_name)[1]
    if module_ext not in valid_header_exts:
        raise ValueError(f"Invalid module file extension. Expected one of: {', '.join(valid_header_exts)}")
    
    module_name = os.path.splitext(module_name)[0]

    return module_name

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
        modules = []
        with open(file_path, 'r') as file:
            for line in file:
        
                if pattern_main_start.search(line):
                    print("Main start found, breaking out of the loop because no imports are allowed after this point.")
                    break
                
                if not pattern_compile.search(line):
                    continue

                line2 = file.readline().strip()
                module_name = extract_module_from_line(line2, valid_header_exts)

                modules.append(module_name)

        for module in modules:
            compile_command += f"-I./c_cpp_modules_dld/{module}/include/ "
            compile_command += f"-L./c_cpp_modules_dld/{module}/bin/ "
            compile_command += f"-l{module} "
        
        return compile_command
    
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def compile_files():
    with open("module_info.json", "r") as f:
        data = json.load(f)

    files = data.get("files", [])

    if not files:
        print("No files to compile.")
        return
    
    for file in files:
        print(compile(file))

        
if __name__ == '__main__':
    # print(compile("C:/work_of_atri/test/example.c")) 
    # compile_files() 
    print(compile("example.c"))             

