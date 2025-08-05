import os

'''
Currently focussing on:
- header files with .h file extension only.
- gcc compiler.
- c files with .c file extension only.

- will expand later once this stabilizes.
'''

def compile(file_path: str):

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    valid_file_exts = ['.c'] # will add more later
    valid_header_exts = ['.h'] # will add more later
    file_name = os.path.basename(file_path)
    file_ext = os.path.splitext(file_name)[1]

    if file_ext not in valid_file_exts:
        raise ValueError(f"The file must be a C source file with one of the following extensions: {', '.join(valid_file_exts)}")

    compile_command = f"gcc {file_name} -o {os.path.splitext(file_name)[0]} "

    try:
        modules = []
        with open(file_path, 'r') as file:
            for line in file:
        
                if '// @cul.mainStart' in line:
                    print("Main start found, breaking out of the loop because no imports are allowed after this point.")
                    break
                
                if not '// @cul.compile' in line:
                    continue

                line2 = file.readline().strip()
                start = line2.index('"')
                end = line2.rindex('"')
                if start == -1 or end == -1 or start >= end:
                    raise ValueError("Invalid compile command format.")
                
                module_name = os.path.basename(line2[start + 1:end])
            
                if not module_name:
                    raise ValueError("Module name cannot be empty.")
                
                module_ext = os.path.splitext(module_name)[1]
                if module_ext not in valid_header_exts:
                    raise ValueError(f"Invalid module file extension. Expected one of: {', '.join(valid_header_exts)}")
                
                module_name = os.path.splitext(module_name)[0]

                modules.append(module_name)

        # set -I flags for each imported module
        for module in modules:
            compile_command += f"-I./c_cpp_modules_dld/{module_name}/include/ "
        
        # set -L flags for each imported module
        for module in modules:
            compile_command += f"-L./c_cpp_modules_dld/{module_name}/bin/ "

        # set -l flags for each imported module
        for module in modules:
            compile_command += f"-l{module} "

        return compile_command
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

        
if __name__ == '__main__':
    print(compile("example.c"))               

