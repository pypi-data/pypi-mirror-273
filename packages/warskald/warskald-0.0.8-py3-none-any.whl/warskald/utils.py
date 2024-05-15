from collections import OrderedDict
import sys, json, subprocess, os
from typing import Literal, Any
from .attr_dict import AttrDict
from datetime import datetime
from ._globals import GLOBALS

p_join = os.path.join
""" Shortcut for os.path.join """

p_exists = os.path.exists
""" Shortcut for os.path.exists """

SubReturn = Literal['out', 'err', 'both']
""" String literal type representing the output choices for cmdx """

class SubReturns:
    """ Enum class for SubReturn values """
    OUT: SubReturn = 'out'
    ERR: SubReturn = 'err'
    BOTH: SubReturn = 'both'
    
def cmdx(cmd: list[str] | str, rtrn: SubReturn = 'out', print_out: bool = True) -> str | tuple[str, str]:
    """ Executes a command and returns the output or error

    Args:
        cmd (list[str] | str): - A list of strings that make up the command or a string that will be split by spaces
        rtrn (SubReturn, optional): What outputs to return. If both, it will return a tuple of (stdout, stderr) . Defaults to 'out'.

    Returns:
        str | tuple[str, str]: The output of the command or a tuple of (stdout, stderr)
    """    
    
    if(isinstance(cmd, str)):
        cmd = cmd.split()
        
    process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    stdout = process.stdout
    stderr = process.stderr
    if(print_out):
        if(stdout):
            print(stdout)
        if(stderr):
            print('\nERROR:\n',stderr)
            
    if rtrn == 'out':
        return process.stdout
    elif rtrn == 'err':
        return process.stderr
    else:
        return process.stdout, process.stderr

def check_prefixes(prefixes: list[str], arg: str) -> str:
    """ Checks if the argument starts with any of the prefixes and returns the best match
    
    Args:
        prefixes (list[str]): - A list of prefixes to check for
        arg (str): - The argument to check

    Returns:
        str: The prefix that best matches the argument or None
            i.e. if the argument is '--name' and the prefixes are ['--', '-'], it will return '--'
    """
    
    matches = []
    
    for prefix in prefixes:
        if arg.startswith(prefix):
            matches.append(prefix)
            
    return max(matches, key=len) if matches else None

def get_prefix_args(prefixes: list[str] = ['--', '-']) -> AttrDict[str, str] | str:
    """ Parses command line arguments that start with a prefix and returns them as a dictionary

    Args:
        prefixes (list[str], optional): Prefixes to check for. Defaults to ['--', '-'].

    Returns:
        AttrDict[str, str] | str: A dictionary of arguments or a single string
    """
        
    parsed_args = AttrDict()
    args = sys.argv[1:]
    
    if(isinstance(prefixes, list)):
        key: str = None
        value: str = None
        for arg in args:
            prefix_match = check_prefixes(prefixes, arg)
            if prefix_match:
                if(key is not None):
                    parsed_args[key] = value.strip() if value is not None else True
                    value = None
                    
                key = arg[len(prefix_match):]
            else:
                value = f'{value} {arg}' if value is not None else arg
                
        if(key is not None and key not in parsed_args):
            parsed_args[key] = value.strip() if value is not None else True
        elif(key is None and value is not None):
            return value.strip()
        
    return parsed_args

def find_item(items: list, predicate: callable) -> Any:
    """ Finds an item in a list that matches the predicate

    Args:
        items (list): list of items to check
        predicate (callable): function that returns True if the item is a match

    Returns:
        Any: The item that matches the predicate or None
    """
        
    return next((item for item in items if predicate(item)), None)

def find_index(items: list, predicate: callable) -> int | None:
    """ Finds the index of an item in a list that matches the predicate

    Args:
        items (list): list of items to check
        predicate (callable): function that returns True if the item is a match

    Returns:
        int | None: The index of the item that matches the predicate or None
    """
        
    return next((i for i, item in enumerate(items) if predicate(item)), None)

def pretty_print(obj: any) -> None:
    """ Prints a JSON serializable object with indentation """
    
    print(json.dumps(obj, indent=4))
                
def get_inputs(prefixes: list[str] = ['--', '-'], arg_names: list[str] = None, options: dict = None) -> AttrDict[str, str] | str:
    """ Parses command line arguments based on the prefix, argument names, and/or options

    Args:
        prefix (list[str], optional): Prefix(es) to check. Defaults to ['--', '-'].
        arg_names (list[str], optional): Specific string values to search for. Defaults to None. *Not implemented yet*
        options (dict, optional): A dictionary of various option values. Defaults to None. *Not implemented yet*

    Returns:
        AttrDict[str, str] | str: A dictionary of arguments or a single string
    """
        
    if(isinstance(options, dict)):
        pass
    elif(isinstance(arg_names, list)):
        pass
    elif(isinstance(prefixes, list)):
        return get_prefix_args(prefixes)

def cap_first(value: str) -> str:
    """ Capitalizes the first letter of a string """
    
    return value[0].upper() + value[1:]

def stringify_float(value: float) -> str:
    """ Formats a float as a string without commas """
    
    return str(value).replace(',','')

def is_numeric(value) -> bool:
    """ Checks if a value is numeric """
    
    try:
        if(isinstance(value, str)):
            value = value.replace(',', '')
        float(value)
        return True
    except Exception:
        
        return False
    
def to_dict(obj: Any, allow_none: bool = True, forbidden_keys: list[str] = [], allow_empty: bool = True, 
            forbidden_values: list[Any] = [], forbidden_types: list[type] = (), forbidden_prefixes: list[str] = [],
            strip_prefixes: list = ['_prop_']) -> Any:
    """ Converts an object to a JSON serializable object

    Args:
        obj (Any): The object to convert
        allow_none (bool, optional): Whether to allow null values. Defaults to True.
        forbidden_keys (list[str], optional): Keys to exclude in the returned dictionary. Defaults to [].
        allow_empty (bool, optional): Whether to allow falsey values (i.e. '', [], etc..). Defaults to True.
        forbidden_values (list[Any], optional): List of specific values to omit from the result. Defaults to [].
        forbidden_types (list[type], optional): List of specific types to omit from the result. Defaults to ().
        forbidden_prefixes (list[str], optional): List of str prefixes to omit if the key starts with them. Defaults to [].
        strip_prefixes (list, optional): Prefixes to remove from keys that have them. Defaults to ['_prop_'].

    Returns:
        Any: Either a dictionary, list, or a primitive value if the object can be converted.
    """    
    
    if(isinstance(obj, list)):
        return [to_dict(
            item, 
            allow_none, 
            forbidden_keys, 
            allow_empty, 
            forbidden_values, 
            forbidden_types, 
            forbidden_prefixes 
            ) for item in obj]
        
    if(isinstance(obj, dict)):
        
        new_dict = {}
        
        for key, value in obj.items():
            
            safe_key = str(key)
            
            if(safe_key in forbidden_keys or key in forbidden_keys):
                continue
            if(value in forbidden_values):
                continue
            if(isinstance(value, forbidden_types)):
                continue
            if(safe_key.startswith(tuple(forbidden_prefixes))):
                continue
            if(value == None and not allow_none):
                continue
            if(not value and value != 0 and not allow_empty):
                continue
            if(strip_prefixes):
                for prefix in strip_prefixes:
                    if(safe_key.startswith(prefix)):
                        safe_key = safe_key[len(prefix):]
                        break
                    
            new_dict[safe_key] = to_dict(
                value, 
                allow_none, 
                forbidden_keys, 
                allow_empty, 
                forbidden_values, 
                forbidden_types, 
                forbidden_prefixes
            )
            
        return new_dict
    
    if(isinstance(obj, datetime)):
        return obj.strftime('%m/%d/%Y')
    
    if(not isinstance(obj, (str, int, float, list, dict)) and hasattr(obj, "__dict__")):
        return to_dict(obj.__dict__, allow_none, forbidden_keys, allow_empty, forbidden_values, forbidden_types, forbidden_prefixes)
    
    return obj

def save_data(data: Any, filename: str, use_global_data_path: bool = True) -> None:
    """ Saves data to a file

    Args:
        data (Any): The data to save
        filename (str): The name or path of the file, including the extension. 
            If use_global_data_path is True, only the filename is needed.
        use_global_data_path (bool, optional): Whether to prepend GLOBALS.DATA_PATH. Defaults to True.
    """
        
    if(use_global_data_path):
        filename = GLOBALS.DATA_PATH + filename
    as_json = filename.endswith('.json') and isinstance(data, (list, dict))
    
    if(as_json):
        with open(filename, 'w') as writer:
            data = to_dict(data)
            writer.write(json.dumps(data, indent=4, ensure_ascii=False))
    else:
        with open(filename, 'w') as writer:
            writer.write(data)
            
FileReturnType = list | dict | str | None
""" A type hint for the return type of load_data """

def load_data(
    filename: str, 
    as_type: type = None, 
    use_global_data_path: bool = True,
    text_lines: bool = False,
    as_bytes: bool = False
    ) -> FileReturnType:
    """ Loads data from a file

    Args:
        filename (str): The name or path of the file, including the extension. 
            If use_global_data_path is True, only the filename is needed.
        as_type (type, optional): Optional type provided to cast the data into. Defaults to None.
        use_global_data_path (bool, optional): Whether or not to prepend filename 
            with GLOBALS.DATA_PATH. Defaults to True.

    Returns:
        FileReturnType: The data from the file
    """
        
    if(use_global_data_path):
        filename = GLOBALS.DATA_PATH + filename
    
    if(not p_exists(filename)):
        return None
    
    file_data = open(filename, 'rb' if as_bytes else 'r')
    if(as_bytes):
        return file_data.read()
    
    result = None
    if(filename.endswith('.json')):
        result = json.load(file_data)
    else:
        result = file_data.readlines() if text_lines else file_data.read() 
        
    result = as_type(result) if as_type else result
    
    return result


def debug_print(*args):
    strings = list(args)
    strings.insert(0, '\n')
    strings.append('\n')
    print(*strings)

def last(arr: list):
    return arr[len(arr) - 1]

def set_nested(obj: dict | list, path: list[str] | str, value: Any, debug: bool = False) -> None:
    if(isinstance(path, str)):
        path = path.split('.')
    
    if(debug):
        debug_print('starting function')
        pretty_print({
            'obj': obj,
            'path': path,
            'value': value
        })
    
    if(len(path) == 1):
        if(isinstance(obj, dict)):
            obj[path[0]] = value
        elif(isinstance(obj, list) and path[0].isdigit()):
            if(int(path[0]) < len(obj)):
                obj[int(path[0])] = value
            else:
                obj.append(value)
                
    else:
        key = path.pop(0)
        
        if(debug): 
            debug_print('key', key)
        
        if(isinstance(obj, list) and key.isdigit()): # true
            if(debug):
                debug_print('obj is list', 'key < len', int(key) < len(obj))
                
            if(int(key) < len(obj)): # 3 < 3 == False
                sub = obj[int(key)]
                if(not sub or not isinstance(sub, (dict, list))):
                    if(debug):
                        debug_print('sub is None or not an object', 'creating new sub')
                        
                    if(path[0].isdigit()):
                        obj[int(key)] = []
                    else:
                        obj[int(key)] = {}
                        
                set_nested(obj[int(key)], path, value)
            else:
                if(debug):
                    debug_print('out of bounds', 'inserting new value', f'path[0] = {path[0]}')
                    
                if(path[0].isdigit()):
                    obj.insert(int(key), [])
                else:
                    obj.insert(int(key), {})
                
                if(debug):
                    debug_print('blank inserted', obj)
                    
                set_nested(last(obj), path, value)
                
        elif(isinstance(obj, dict)):
            sub = obj.get(key)
            
            if(debug):
                debug_print('obj is dict', 'sub:', sub)
                
            if(not sub or not isinstance(sub, (dict, list))):
                if(debug):
                    debug_print('sub is None or not an object', 'creating new sub')
                    
                if(path[0].isdigit()):
                    obj[key] = []
                else:
                    obj[key] = {}
                
                if(debug):
                    debug_print('new sub created', obj)
            
            set_nested(obj.get(key), path, value)
        
def get_nested(obj: dict | list, path: list[str] | str) -> Any:
    if(isinstance(path, str)):
        path = path.split('.')
        
    if(len(path) == 1):
        if(isinstance(obj, dict)):
            return obj.get(path[0])
        elif(isinstance(obj, list) and path[0].isdigit()):
            return obj[int(path[0])]
    else:
        key = path.pop(0)
        if(isinstance(obj, list) and key.isdigit()):
            if(int(key) < len(obj)):
                return get_nested(obj[int(key)], path)
            return None
        if(key not in obj):
            return None
        return get_nested(obj[key], path)
    
def reorder_dict_by_value_len(obj: dict) -> dict:
    return dict(OrderedDict(sorted(obj.items(), key=lambda item: len(item[1]), reverse=True)))