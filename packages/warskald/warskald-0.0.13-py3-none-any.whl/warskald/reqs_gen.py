from __future__ import annotations
import os, sys, subprocess, re
from typing import Any
from fuzzywuzzy import fuzz

help_text = '''Usages:
    
    python reqs_gen.py
        With no args, the script will assume the current directory as the path to the app. 
        It will search recursively through all files, scanning for import statements and check them
        against the installed packages. It will then generate a requirements.txt file with the
        installed packages.
    
    Command Line Arguments:
        Note: order of arguments does not matter, other than that --path and --output must be followed
        by the path and output file, respectively.        
    
    --help
        Prints out a list of commands and their descriptions.
        
    --path <path_to_app>
        If the path is a directory, the script will search recursively through all files in the specified 
        path, scanning for import statements and check them against the installed packages. It will then 
        generate a requirements.txt file with the installed packages and save it to the specified path.
        
        If the path is a file, it will only scan that file for imports. Additionally, the requirements.txt
        file will be saved to the same directory as the file.
        
    --output <output_file>
        The script will generate a requirements.txt file with the installed packages and save it to the
        specified output file. If the output file already exists, new imports will be appended to the file,
        and existing imports will be updated.        
        
    --overwrite
        If this flag is set, the script will overwrite the output file if it already exists. If the flag is
        not set
'''

PIP_LIST: set[tuple[str, str]] = set()
BASE_REQS = [
    'blinker',
    'click',
    'colorama',
    'itsdangerous',
    'Jinja2',
    'MarkupSafe',
    'Werkzeug',
]

def process_args():
    args = sys.argv
    path = None
    output = None
    overwrite = False
    
    skip_next = False
    
    if(len(args) > 1):
        for i in range(1, len(args)):
            if(args[i] == '--help'):
                print(help_text)
                return
            elif(args[i] == '--path'):
                path = args[i+1]
                skip_next = True
            elif(args[i] == '--output'):
                output = args[i+1]
                skip_next = True
            elif(args[i] == '--overwrite'):
                overwrite = True
            else:
                if(skip_next):
                    skip_next = False
                    continue
                else:
                    print(f'Invalid argument {args[i]}')
                    return
                
    path = os.getcwd() if path == None else path
    output = os.path.join(path, 'requirements.txt') if output == None else output

    return path, output, overwrite

def execute(cmd: str | list[str]) -> str:
    """ Execute a command and return the output as a string.

    Args:
        cmd (str | list[str]): The command to execute. If a string, it will be split into a list.

    Returns:
        str: The output of the command.
    """
        
    if(isinstance(cmd, str)):
        cmd = cmd.split()
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        print(f'Error executing command: {cmd}')
        print(e)
        return None
    
def get_pip_list() -> list[tuple[str, str]]:
    """ Get a list of installed packages and their versions.

    Returns:
        list[tuple[str, str]]: A list of tuples, where the first element is the package name and the second
        element is the version.
    """
    
    pip_list = execute('pip list')
    if(pip_list == None):
        return None
    
    pip_list = pip_list.split('\n')
    pip_list = pip_list[2:-1]
    for package in pip_list:
        PIP_LIST.add(tuple(package.split()))

def get_package_data(package_name: str) -> tuple[str, str] | None:
    """ Get the version of an installed package.

    Args:
        package_name (str): The name of the package.

    Returns:
        tuple[str, str] | None: A tuple where the first element is the package name and the second element is the
        version. If the package is not installed, None is returned.
    """
    
    for package in PIP_LIST:
        if(fuzz.ratio(package_name.lower(), package[0].lower()) > 80):
            return package
    return None

def parse_dir_imports(directory: str) -> list[tuple[str, str]]:
    """ Parse a directory for import statements.

    Args:
        directory (str): The directory to parse.

    Returns:
        list[tuple[str, str]]: A list of tuples, where the first element is the package name and the second
        element is the version.
    """
    
    package_names = []
    
    if(os.path.exists(directory) == False):
        print(f'Directory {directory} does not exist')
        return None
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            package_names.extend(parse_file_imports(os.path.join(root, file)))
            
    return package_names
    
def parse_file_imports(file: str) -> list[tuple[str, str]]:
    """ Parse a file for import statements.

    Args:
        file (str): The file to parse.

    Returns:
        list[tuple[str, str]]: A list of tuples, where the first element is the package name and the second
        element is the version.
    """
    package_names = []
    
    if(os.path.exists(file) == False):
        print(f'File {file} does not exist')
        return None
    
    with open(file, 'r') as reader:
        lines = reader.readlines()
        from_pattern = r'from\s+(\w+)\s+import\s+'
        import_pattern = r'import\s+(.*)'
        
        for line in lines:
            if(line.startswith('from')):
                matches = re.findall(from_pattern, line)
                if(len(matches) > 0):
                    package_names.extend(matches)
            elif(line.startswith('import')):
                matches = re.findall(import_pattern, line)
                if(len(matches) > 0):
                    
                    package_names.extend([ x.strip() for x in matches[0].split(',') ])
                    
    packages: list[tuple[str, str]] = parse_names_to_reqs(package_names)
                    
    return packages

def parse_names_to_reqs(package_names: list[str]) -> list[tuple[str, str]]:
    """ Parse a list of package names to a list of tuples, where the first element is the package name and the
    second element is the version.

    Args:
        package_names (list[str]): A list of package names.

    Returns:
        list[tuple[str, str]]: A list of tuples, where the first element is the package name and the second
        element is the version.
    """
    
    reqs = []
    for package in package_names:
        req = get_package_data(package)
        if(req is not None):
            reqs.append(req)
            
    return reqs

def write_requirements(reqs: list[tuple[str, str]], output: str, overwrite: bool = False):
    """ Write a list of package names and versions to a requirements.txt file.

    Args:
        reqs (list[tuple[str, str]]): A list of tuples, where the first element is the package name and the second
        element is the version.
        output (str): The path to the output file.
        overwrite (bool, optional): If True, the output file will be overwritten if it already exists. Defaults to False.
    """
    print('conditions:', os.path.exists(output), overwrite)
    if(os.path.exists(output) and overwrite == False):
        with open(output, 'a') as writer:
            for req in reqs:
                writer.write(f'{req[0]}=={req[1]}\n')
                return
    
    with open(output, 'w') as writer:
        for req in reqs:
            writer.write(f'{req[0]}=={req[1]}\n')

def is_list_tuple(obj: Any) -> bool:
    return isinstance(obj, list) and all(isinstance(x, tuple) for x in obj)

def main():
    args = process_args()
    if(isinstance(args, tuple)):
        path, output, overwrite = args
        if(path == None or output == None):
            return
        
        get_pip_list()
         
        req_list = parse_names_to_reqs(BASE_REQS)
        
        if(os.path.isfile(path)):
            req_list.extend(parse_file_imports(path))
        if(os.path.isdir(path)):
            req_list.extend(parse_dir_imports(path))
        
        if(is_list_tuple(req_list)):
            write_requirements(req_list, output, overwrite)
    

if(__name__ == '__main__'):
    main()