import re
from ._globals import GLOBALS
from .utils import is_numeric
from typing import Any
from flask import request, g, has_request_context


def parse_str_type(value: str, empty_value: Any = 0):
    if(isinstance(value, str)):
        if(re.search(GLOBALS.DOUBLE_QUOTE_PATTERN, value)):
            return value.strip().strip('"')
        
        if(re.search(GLOBALS.SINGLE_QUOTE_PATTERN, value)):
            return value.strip().strip("'")
        
        if(re.search(GLOBALS.LIST_STR_PATTERN, value)):
            return list_str_to_list(value)
        
        value = value.strip().replace(',', '')
        
        if(is_numeric(value)):
            if('.' in value):
                return float(value)
            return int(value)
        
        if(value.lower() == 'true'):
            return True
        
        if(value.lower() == 'false'):
            return False
    
        if(value.strip() == ''):
            return empty_value
        
    return value

def list_str_to_list(list_str: str):
    search = re.search(GLOBALS.LIST_STR_PATTERN, list_str)
    
    if(search):
        parsed_list = []
        list_str = search.group(1)
        
        list_split = list_str.split(',')
        
        for item in list_split:
            parsed_list.append(parse_str_type(item))
            
        return parsed_list
    return list_str

def parse_request_data():
    if(has_request_context() and request):
        g.request_data = {}
        
        if(request.method == 'GET'):
            for key, value in request.args.items():
                g.request_data[key] = parse_str_type(value)
        else:    
            g.request_data = request.get_json()
            
        return g.request_data