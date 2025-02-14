import subprocess

def extract_header_files(filename):
    with open(filename, "r") as file:
        headers = set()
        for line in file:
            line = line.strip()
            if line.startswith("#include") and 'c_cpp_modules_dld' in line and '.h"' in line:
                parts = line.split('"')
                if len(parts) >= 2 and "/" in parts[1]:
                    headers.add(parts[1].split("/")[-1])
    return headers

def prepare_compile_command(filename, headers):
    compile_command = f"gcc {filename}" 
    for header in headers:
        compile_command += f" -I./c_cpp_modules_dld/{header.split('.')[0]} -L./c_cpp_modules_dld/{header.split('.')[0]}"
        compile_command += f" -l{header.split('.')[0]}"
    compile_command += f" -o {filename.split('.')[0]}"
    return compile_command

# commands i ran to compile this successfully:
# gcc/g++ file_name.c/.cpp -Idir_of_dot_h -Ldir_of_dot_h -lname_of_a_without_lib_in_front -o desired_file_name_in_output.exe

# in case of multiple libraries
# g++ main.cpp -I./dir1 -I./dir2 -L./dir1 -L./dir2 -lbgi -lotherlib -o output.exe

# Example usage
filename = "main.c"
headers = extract_header_files(filename)
print("Header files found:", headers)
compile_command = prepare_compile_command(filename, headers)
print("Compile command:", compile_command)
subprocess.run(compile_command, shell=True)
subprocess.run("main.exe", shell=True)  # Run the compiled executable