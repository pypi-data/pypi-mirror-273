import os

class GLOBALS:
    """ Configurable global variables """
    LIST_STR_PATTERN = r'^\[(.*)\]$'
    SINGLE_QUOTE_PATTERN = r"^'(.*)'$"
    DOUBLE_QUOTE_PATTERN = r'^"(.*)"$'
    
    DATA_PATH = os.path.join(os.getcwd(), '/data/')
    PORTS_FILE = '/home/joseph/coding_base/configs/ports.json'