import os, sys, utils, regex
from caseconverter import snakecase, kebabcase, camelcase
from .attr_dict import AttrDict
from typing import Any, Callable
import inspect
import functools

exists = os.path.exists
""" shortcut for os.path.exists """

p_join = os.path.join
""" shortcut for os.path.join """

# region Global Variables
DIR = os.getcwd()

TEMP_DIR = p_join(os.path.dirname(__file__), 'temp')
""" Path to the temp directory """

MODELS_PATH = '/home/joseph/coding_base/ws-ui-2/src/app/models'
""" May need to generalize this later """

P_CONFIGS_PATH = p_join(MODELS_PATH, 'prime_configs')
""" Path to the PrimeNG config interfaces """

P_CONFIG_INDEX = p_join(P_CONFIGS_PATH, '_index.ts')
""" Path to the PrimeNG config index file """

COMPS_PATH = '/home/joseph/coding_base/ws-ui-2/src/app/components'
""" Path to the components directory"""

COMPS_INDEX = f'{COMPS_PATH}/_index.ts'
""" Path to the component index file """


class GLOBALS:
    """ Global variables for the script """
    
    test_mode: bool = False
    debug: bool = False
    prime_name: str = None
    prime_capped: str = None
    widget_config: str = None
    widget_name: str = None
    widget_comp_name: str = None
    element_type: str = None
    prime_text: str = None
    html_template: str = None
    prime_config: str = None
    p_config_name: str = None
    
    DIR = DIR
    MODELS_PATH = MODELS_PATH
    P_CONFIGS_PATH = P_CONFIGS_PATH
    P_CONFIG_INDEX = P_CONFIG_INDEX
    COMPS_INDEX = COMPS_INDEX
    COMPS_PATH = COMPS_PATH
    ELEMENT_CONFIGS = p_join(MODELS_PATH, 'element-configs.ts')
    ELEMENT_TYPES = p_join(MODELS_PATH, 'element-types.ts')
    HTML_PATH = None
    WIDGET_COMP_PATH = None
    STYLE_PATH = None
    
    
TEMPLATE = open('/home/joseph/coding_base/scripts/utils/templates/ngwidget.txt', 'r').read()
""" Template for the widget component """

TEMPLATE_VALS: AttrDict = AttrDict({
    '{base_type}': 'unknown',
    '{base_value}': 'undefined',
    '{cva_impl}': '',
    '{cva_import}': '',
    '{cva_provider}': '',
    '{reactive_import}': '',
    '{cva_inputs}': '',
    '{cva_inner_ctl}': '',
    '{cva_inner_ctl_init}': '',
    '{cva_functs}': '',
    '{element_type}': 'COMPONENT',
    '{options}': '\n    @Input() options?: WeakObject = {};\n',
    '{outputs}': '',
    '{prime_config}': '',
    '{prime_import}': '',
    '{prime_module}': '',
    '{reactive_import}': '',
    '{view_child}': '',
})
""" Dictionary containing search/replace values for the widget template """

IMPORT_PATTERN = r'import \{.+?\} from \'.+?\';'
""" Regex pattern for TS imports """

EXPORT_PATTERN = r'export \* from \'.+?\';'
""" Regex pattern for TS exports"""

PRIME_PATH = '/home/joseph/coding_base/primeng17/primeng-17.16.0/src/app/components'
""" Path to the local PrimeNG source code """

SELECTOR_PATTERN = r'selector: \'(.+?)\''
""" Pattern to retrieve the component selector from the PrimeNG module """

# endregion Global Variables


# region General Functions
def debug(*args):
    """ Prints debug information if debug mode is enabled """
    
    if(GLOBALS.debug):
        print(*args)
        
def debug_pretty(obj: Any):
    """ Prints debug information if debug mode is enabled """
    
    if(GLOBALS.debug):
        utils.pretty_print(obj)
        
def debuggable(func: Callable[..., Any]) -> Callable[..., Any]:
    """ Decorator function to print debug information for a function

    Args:
        func (Callable[..., Any]): The function to decorate

    Returns:
        Callable[..., Any]: The decorated function
    """
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get the original function signature (i.e., its args and kwargs)
        sig = inspect.signature(func)

        # Print the entry statement with all passed arguments
        debug(f"Calling {func.__name__} with:")
        for arg_name, arg_value in zip(sig.parameters.keys(), args + tuple(kwargs.values())):
            debug(f"{arg_name}={arg_value},")
        debug("\n")
        
        return_val = None
        
        try:
            return_val = func(*args, **kwargs)
        except Exception as e:
            print('ERROR:',e)
            return_val = None
            
        debug(f'Function {func.__name__} returned: {return_val}\n')
        return return_val
    
    return wrapper
              
def uniq(arr: list) -> list:
    """ Returns a list with all duplicate values removed

    Args:
        arr (list): The list to remove duplicates from

    Returns:
        list: A list with all duplicate values removed
    """
    
    return list(set(arr))

def search_replace(text: str, values: dict) -> str:
    for key, value in values.items():
        text = text.replace(key, value)
        
    return text

def write_file(path: str, text: str, mode: str = 'w') -> None:
    """ Writes text to a file

    Args:
        path (str): The path to the file to write to
        text (str): The text to write to the file

    Returns:
        None
    """
    debug(f'Writing to file: {path}')
    writer = open(path, mode)
    writer.write(text)
    writer.close()
# endregion General Functions

# region PrimeNG Functions
@debuggable
def get_comp_path() -> str:
    prime_module = GLOBALS.prime_name.lower()
    if(prime_module):
        path = p_join(PRIME_PATH, f'{prime_module}', f'{prime_module}.ts')
        debug(path)
        return path

@debuggable
def get_comp() -> None:
    comp_path = get_comp_path()
    
    if(comp_path and exists(comp_path)):
        GLOBALS.prime_text = open(comp_path, 'r').read()

@debuggable
def get_selectors() -> list[str]:
    return regex.findall(SELECTOR_PATTERN, GLOBALS.prime_text)

@debuggable
def get_selector() -> tuple[str,list[str]]:
    """ Gets the selector for a PrimeNG module

    Returns:
        str: The selector for the PrimeNG module
    """
    
    selectors = get_selectors()
    
    debug('at get_selectors: len(selectors) =', len(selectors))
    if(len(selectors) > 1):
        print('Found multiple selectors, choose the one to use:')
        
        [ print(f'{i + 1}. {selector}') for i, selector in enumerate(selectors) ]
        
        choice = None
        choice_valid = False
        
        def get_choice(print_str: str) -> int | str:
            try:
                return int(input(print_str))
            except Exception as inst:
                if(isinstance(inst, ValueError)):
                    return ''
                else:
                    print(inst)
                    return ''
                
        while(not choice_valid):
            if(choice is None):
                choice = get_choice('Enter the number of the selector to use: ')
            else:
                choice = get_choice('Invalid input, enter the number of the selector to use: ')
            
            if(isinstance(choice, int) and choice > 0 and choice <= len(selectors)):
                choice_valid = True
                
        selector = selectors[choice - 1]
    else:
        selector = selectors[0]
        
    return selector, selectors

@debuggable
def get_prime_values() -> list[tuple]:
    """ Attempts to get the input properties from a PrimeNG module

    Returns:
        list[tuple]: list of tuples representing the input properties in an HTML template
            tuple structure: (name, type, default_value)
    """
    
    comp = GLOBALS.prime_text
    
    selector, selectors = get_selector()
    
    selector_idxs = {selector: comp.index(f'selector: \'{selector}\'') for selector in selectors}
    
    start_idx = selector_idxs.get(selector, 0)
    
    selector_idx = selectors.index(selector)
    next_selector = selectors[selector_idx + 1] if selector_idx + 1 < len(selectors) else ''
    
    end_idx = selector_idxs.get(next_selector, len(comp))
    
    comp = comp[start_idx:end_idx]
    
    input_pattern = r'@Input\(.*\)\s(\w+?):\s(.+?)(?(?= =)\s=\s(.+?)())[;\n&]'
    input_matches = regex.findall(input_pattern, comp)
    input_matches = [(match[0], match[1], match[2]) for match in input_matches]
    
    output_pattern = r'@Output\(\) (\w+?): EventEmitter\<(\w+?)\>'
    output_matches = regex.findall(output_pattern, comp)
    output_matches = [(match[0], match[1]) for match in output_matches]
    
    return input_matches, output_matches, selector

@debuggable
def check_if_form() -> bool:
    """ Checks if a PrimeNG module is a form component

    Returns:
        bool: True if the module is a form component, False otherwise
    """
        
    comp = GLOBALS.prime_text
    
    val_accessor = f'{GLOBALS.prime_name.upper()}_VALUE_ACCESSOR'
    form_pattern = rf'export const {val_accessor}:'
    
    return regex.search(form_pattern, comp) is not None

@debuggable
def build_prime_templates() -> tuple[str]:
    """ Builds the HTML template and config interface for a PrimeNG module

    Returns:
        None
    """

    common_bools = [
        'disabled',
        'required'
    ]
        
    input_vals, output_vals, selector = get_prime_values()
        
    html_template = f'<{selector} #{GLOBALS.prime_name}Ref'
    
    parent_type = 'BaseComponentConfig'
    
    if(check_if_form()):
        html_template += '\n    [formControl]="innerControl"'
        parent_type = 'FormElementConfig' 
        add_cva_to_template()
    
    prime_config_name = f'P{GLOBALS.prime_capped}Config'
        
    prime_config = f'export interface {prime_config_name} {{\n'
    
    widget_config = f'export interface {GLOBALS.widget_comp_name}Config extends {parent_type} {{\n'
    widget_config += f'    elementType: ElementType.{GLOBALS.element_type};\n'
    widget_config += f'    options?: PrimeConfigs.{prime_config_name};\n'
    
    outputs = '\n'
    
        
    for item in input_vals:
        input_name, data_type, default_value = item
        
        data_type = data_type.replace('any', 'unknown')
        
        html_template += f'\n    [{input_name}]="options.{input_name}'
        prime_config += f'    {input_name}?: {data_type};\n'
        
        if(input_name in common_bools):
            default_value = 'false'
        if(default_value):
            html_template += f' ?? {default_value}"'
        else:
            html_template += '"'
            
    for item in output_vals:
        output_name, data_type = item
        data_type = data_type.replace('any', 'unknown')
        
        html_template += f'\n    ({output_name})="{output_name}Handler($event)"'
        widget_config += f'\n    {camelcase(output_name)}Handler?: (event: {data_type}) => void;'
        outputs += f'\n    @Input() {camelcase(output_name)}Handler(event: {data_type}): void {{}}\n'
            
    html_template += f'>\n</{selector}>\n'
    prime_config += '\n    [key: string]: unknown;\n'
    prime_config += '}\n'
    widget_config += '\n}\n'
    
    GLOBALS.html_template = html_template
    GLOBALS.prime_config = prime_config
    GLOBALS.widget_config = widget_config
    TEMPLATE_VALS['{outputs}'] = outputs

@debuggable
def write_prime_templates() -> None:
    """ Writes the HTML template and PrimeNG config interface to files

    Args:
        html_template (str):  The HTML template for the widget
        prime_config (str):  The PrimeNG config interface for the widget
        name (str):  The name of the widget
        prime_module (str):  The PrimeNG module to import
        element_type (str): The ElementType enum key to use for the widget
    """    
    if(GLOBALS.html_template):
        write_file(GLOBALS.HTML_PATH, GLOBALS.html_template)
    
    if(GLOBALS.prime_config):
        config_file = f'p-{kebabcase(GLOBALS.prime_name).lower()}'
        
        GLOBALS.p_config_name = config_file
        
        config_path = p_join(GLOBALS.P_CONFIGS_PATH, f'{config_file}.ts')
    
        write_file(config_path, GLOBALS.prime_config)
        
        update_index_file(GLOBALS.P_CONFIG_INDEX)

# endregion PrimeNG Functions

# region Widget Functions

@debuggable
def configure_temp_dir():
    """ Configures the temp directory for the script

    Returns:
        None
    """
    
    exec = utils.cmdx
    
    print('Clearing temp directory...')
    utils.cmdx(f'rm -rf {TEMP_DIR}')
    
    print('Creating temp directory...')
    os.mkdir(TEMP_DIR)
        
    ORG_COMPS_INDEX = GLOBALS.COMPS_INDEX
    ORG_P_CONFIG_INDEX = GLOBALS.P_CONFIG_INDEX
    ORG_ELEMENT_CONFIGS = GLOBALS.ELEMENT_CONFIGS
    ORG_ELEMENT_TYPES = GLOBALS.ELEMENT_TYPES
    ORG_P_CONFIGS_PATH = GLOBALS.P_CONFIGS_PATH
      
    GLOBALS.MODELS_PATH = p_join(TEMP_DIR, 'models')
    GLOBALS.ELEMENT_TYPES = p_join(GLOBALS.MODELS_PATH, 'element-types.ts')
    GLOBALS.ELEMENT_CONFIGS = p_join(GLOBALS.MODELS_PATH, 'element-configs.ts')
    
    GLOBALS.P_CONFIGS_PATH = p_join(GLOBALS.MODELS_PATH, 'prime_configs')
    GLOBALS.P_CONFIG_INDEX = p_join(GLOBALS.P_CONFIGS_PATH, '_index.ts')
    
    GLOBALS.COMPS_PATH = p_join(TEMP_DIR, 'components')
    GLOBALS.COMPS_INDEX = p_join(GLOBALS.COMPS_PATH,'_index.ts')
    
    temp_comps = p_join(GLOBALS.COMPS_PATH, GLOBALS.widget_name)
    GLOBALS.WIDGET_COMP_PATH = p_join(temp_comps, f'{GLOBALS.widget_name}.component.ts')
    GLOBALS.HTML_PATH = p_join(temp_comps, f'{GLOBALS.widget_name}.component.html')
    GLOBALS.STYLE_PATH = p_join(temp_comps, f'{GLOBALS.widget_name}.component.scss')
    
    os.makedirs(GLOBALS.P_CONFIGS_PATH)
    os.makedirs(GLOBALS.COMPS_PATH)
    
    def touch(path: str):
        dir_name = os.path.dirname(path)
        os.makedirs(dir_name, exist_ok=True)
        open(path, 'w').close()
        
    touch(GLOBALS.WIDGET_COMP_PATH)
    touch(GLOBALS.HTML_PATH)
    touch(GLOBALS.STYLE_PATH)
    touch(GLOBALS.P_CONFIG_INDEX)
    touch(GLOBALS.COMPS_INDEX)
    touch(GLOBALS.ELEMENT_CONFIGS)
    touch(GLOBALS.ELEMENT_TYPES)
    
    exec(f'cp {ORG_COMPS_INDEX} {GLOBALS.COMPS_INDEX}')
    exec(f'cp {ORG_P_CONFIG_INDEX} {GLOBALS.P_CONFIG_INDEX}')
    exec(f'cp {ORG_ELEMENT_CONFIGS} {GLOBALS.ELEMENT_CONFIGS}')
    exec(f'cp {ORG_ELEMENT_TYPES} {GLOBALS.ELEMENT_TYPES}')
    
    for file in os.listdir(ORG_P_CONFIGS_PATH):
        if(not file.startswith('_')):
            exec(f'cp {p_join(ORG_P_CONFIGS_PATH, file)} {p_join(GLOBALS.P_CONFIGS_PATH, file)}')

@debuggable        
def build_widget_config():
    """ Builds the widget configuration interface

    Returns:
        None
    """
    
    widget_configs_path = GLOBALS.ELEMENT_CONFIGS
    widget_config = GLOBALS.widget_config
    
    if(exists(widget_configs_path) and widget_config):
        full_text = open(widget_configs_path, 'r').read()
        
        union_start_idx = full_text.index('/**\n * Union type of all')
        
        comps_text = full_text[:union_start_idx]
        if(widget_config not in comps_text):
            comps_text += f'\n{widget_config}\n'
        
        union_text = full_text[union_start_idx:]
        
        config_pattern = r'export interface (\w+?) extends'
        config_names = uniq(regex.findall(config_pattern, comps_text))
        config_names.sort()
        
        union_text = '/**\n * Union type of all possible element configs\n */\nexport type ComponentConfig = '
        for i, config_name in enumerate(config_names):
            union_text += f'\n    {config_name} |' if i < len(config_names) - 1 else f'\n    {config_name};'
            
        write_file(widget_configs_path, comps_text + union_text)

@debuggable
def update_element_types() -> None:
    """ Updates the ElementType enum with a new element type

    Returns:
        None
    """
    
    element_type = GLOBALS.element_type
    element_path = GLOBALS.ELEMENT_TYPES
    
    if(exists(element_path) and isinstance(element_type, str)):
        element_type = element_type.upper()
        element_text = open(element_path, 'r').read()
        
        enum_start_idx = element_text.index('export enum ElementType {')
        
        enum_end_idx = element_text.index('}')
        
        enum_text = element_text[enum_start_idx:enum_end_idx]
        
        element_types = regex.findall(r'(\w+?)\s=\s\'(.+?)\'', enum_text)
        
        element_types.append((element_type, kebabcase(element_type).lower()))
        element_types = uniq(element_types)
        element_types.sort(key=lambda item: item[0])
        
        enum_text = 'export enum ElementType {\n'
        for (key, value) in element_types:
            enum_text += f'    {key} = \'{value}\',\n'
            
        enum_text += '}'
        
        write_file(element_path, enum_text)

@debuggable
def get_default_ts_value(base_type: str) -> str:
    """ Returns the default value for a Typescript type

    Args:
        base_type (str): - The base type to get the default value for

    Returns:
        str: The default value for the base type
    """
        
    if(base_type == 'string'):
        return "''"
    elif(base_type == 'number'):
        return '0'
    elif(base_type == 'boolean'):
        return 'false'
    elif(base_type.endswith('[]')):
        return '[]'
    else:
        return 'undefined'

@debuggable
def add_cva_to_template():
    base_type = TEMPLATE_VALS['{base_type}']
    base_value = TEMPLATE_VALS['{base_value}']
    TEMPLATE_VALS['{cva_impl}'] = ', ControlValueAccessor'
    TEMPLATE_VALS['{cva_import}'] = '\nimport { ControlValueAccessor, FormControl, FormGroup, NG_VALUE_ACCESSOR, ReactiveFormsModule } from \'@angular/forms\';'
    TEMPLATE_VALS['{cva_provider}'] = f'\n    providers: [\n        {{\n            provide: NG_VALUE_ACCESSOR,\n            useExisting: forwardRef(() => {GLOBALS.widget_comp_name}Component),\n            multi: true\n        }}\n    ],'
    TEMPLATE_VALS['{reactive_import}'] = '\n        ReactiveFormsModule,'
    TEMPLATE_VALS['{cva_inputs}'] = '\n\n    @Input() onChanged: GenericFunction<void> = () => {};\n\n    @Input() onTouched: GenericFunction<void> = () => {};'
    TEMPLATE_VALS['{cva_inner_ctl}'] = f'\n    public innerControl: FormControl = new FormControl({base_value});\n'
    TEMPLATE_VALS['{cva_inner_ctl_init}'] = '\n\n        this.innerControl = new FormControl(this.value);\n        this.innerControl.valueChanges.subscribe((value) => {\n            this.onChanged(value);\n            this.onTouched(value);\n            this.writeValue(value);\n        });'
    TEMPLATE_VALS['{cva_functs}'] = '\n'.join([
    '\n',
    f'    public writeValue(obj: {base_type}): void {{',
    '        this.value = obj;',
    '        this.form?.patchValue(this.value);',
    '    }',
    '',
    '    public registerOnChange(fn: GenericFunction<unknown>): void {',
    '        this.onChange = fn;',
    '    }',
    '',
    '    public registerOnTouched(fn: GenericFunction<unknown>): void {',
    '        this.onTouched = fn;',
    '    }',
    '',
    '    public setDisabledState?(isDisabled: boolean): void {',
    '        isDisabled ? this.innerControl?.disable() : this.innerControl?.enable();',
    '    }',
    ])
@debuggable
def get_template_vals() -> dict:
    """ Returns the template values for the widget based on command line arguments

    Returns:
        dict: The template values for the widget
    """
        
    args = utils.get_prefix_args()
    
    if('help' in args or 'h' in args):
        print('Usage: ngwidget [options]')
        print('Options:')
        print('  --help [-h] - Display this help message')
        print('  --type [-t] - The Typescript type to use for the widget')
        print('  --value [-v] - The default value of the widget FormControl')
        print('  --name [-n] - The name of the widget')
        print('  --prime_import [-p] - The module form PrimeNG to import (minus "Module" at the end)')
        print('  --element_type [-e] - The ElementType enum key to use for the widget (default: "COMPONENT")')
        print('  --el_from_name [-f] - Use the name of the widget to determine the ElementType enum key')
        print('  --remove_existing [-r] - Remove existing widget files before creating the new widget')
        print('  --is-cva [-c] - Add ControlValueAccessor implementation to the widget')
        print('  --use-formgroup [-g] - Use a FormGroup for the widget. Requires --is-cva. If not provided, uses a FormControl')
        print(f'  --test [-T] - Run the script in test mode, this will create the files locally at {GLOBALS.DIR}/temp and not modify any code in the src project')
        print('  --debug [-d] - Enable debug mode')
        print('Example: ngwidget -t string -v "Hello, World!" -n "greeting" -p "inputtext" -e "COMPONENT"')
        

        sys.exit(0)
        
    print('Building template values...')
    
    name = None
    
    if(args.name or args.n):
        name = args.get('name', args.n)
        
        GLOBALS.widget_comp_name = utils.cap_first(camelcase(name))
        GLOBALS.widget_name = name
        GLOBALS.WIDGET_COMP_PATH = p_join(GLOBALS.DIR, name, f'{name}.component.ts')
        GLOBALS.HTML_PATH = p_join(GLOBALS.DIR, name, f'{name}.component.html')
        TEMPLATE_VALS['{lower_name}'] = name.lower()
        TEMPLATE_VALS['{comp_name}'] = GLOBALS.widget_comp_name
    else:
        print('Error: No name provided for the widget')
        sys.exit(1)
    
    GLOBALS.test_mode = args.get('test', args.T)
    GLOBALS.debug = args.get('debug', args.d)
        
        
    if(args.get('remove_existing', args.r)):
        if(not GLOBALS.test_mode):
            utils.cmdx(f'rm -rf {GLOBALS.DIR}/{name}')
            utils.cmdx(f'rm -rf {GLOBALS.MODELS_PATH}/prime_configs/p-{kebabcase(name).lower()}.ts')
        
    if(args.type or args.t):
        base_type = args.get('type', args.t)
        TEMPLATE_VALS['{base_value}'] = get_default_ts_value(base_type)
        TEMPLATE_VALS['{base_type}'] = base_type
        
    if(args.value or args.v):
        base_value = args.get('value', args.v)
        
        if(not base_value and TEMPLATE_VALS['{base_type}']):
            base_value = get_default_ts_value(base_type)
        TEMPLATE_VALS['{base_value}'] = base_value
    
    if(args.element_type or args.e):
        GLOBALS.element_type = args.get('element_type', args.e).upper()
    elif(args.el_from_name or args.f):
        GLOBALS.element_type = snakecase(name).upper()
        
    TEMPLATE_VALS['{element_type}'] = GLOBALS.element_type 
        
    if(args.is_cva or args.c):
        add_cva_to_template()
    
    if(GLOBALS.test_mode):
        print('Running in test mode...')
        configure_temp_dir()
        
    if(args.prime_import or args.p):
        prime_name = args.get('prime_import', args.p)
        GLOBALS.prime_name = prime_name
        
        module_upper = utils.cap_first(camelcase(prime_name))
        GLOBALS.prime_capped = module_upper
        
        get_comp()
        
        import_str = f'import {{ {module_upper}, {module_upper}Module }} from \'primeng/{prime_name.lower()}\';'
        
        TEMPLATE_VALS['{prime_import}'] = import_str
        TEMPLATE_VALS['{prime_module}'] = f'\n    {module_upper}Module,'
        TEMPLATE_VALS['{prime_config}'] = f', P{module_upper}Config'
        TEMPLATE_VALS['{options}'] = f'\n    @Input() options: P{module_upper}Config = {{}};\n'
        TEMPLATE_VALS['{view_child}'] = f'\n    @ViewChild(\'{prime_name}Ref\') {prime_name}Ref?: {module_upper};\n'

@debuggable
def update_index_file(path: str):
    """ Updates the index file with the new widget

    Args:
        template_vals (dict): The template values for the widget
    """
        
    comp_name = GLOBALS.widget_comp_name
    widget_name = GLOBALS.widget_name
    element_type = GLOBALS.element_type
    
    print(f'Updating index file: {path}')
    print(f'Component Name: {comp_name}')
    
    print('Writing to index file...')
    if(exists(path)):
        if(path != GLOBALS.COMPS_INDEX):
            config_names = os.listdir(GLOBALS.P_CONFIGS_PATH)
            export_lines = []
            for config_name in config_names:
                if(not config_name.startswith('_')):
                    config_name = config_name[:-3] if config_name.endswith('.ts') else config_name
                    
                    export_lines.append(f'export * from \'./{config_name}\';\n')
            export_lines = uniq(export_lines)
            export_lines.sort()
            write_file(path, ''.join(export_lines))
            
        else:
            index_lines = open(path, 'r').readlines()
            
            export_lines = [line for line in index_lines if regex.match(EXPORT_PATTERN, line)]
            export_last_line = index_lines.index(export_lines[-1]) + 1
            
            export_lines.append(f'export * from \'./{widget_name}/{widget_name}.component\';\n')
                
            export_lines = uniq(export_lines)
            export_lines.sort()
            
            import_lines = [line for line in index_lines if regex.match(IMPORT_PATTERN, line)]
            map_lines = index_lines[export_last_line:]
            map_lines = list(filter(lambda line: line.strip(), map_lines))
            map_end_index = utils.find_index(map_lines, lambda line: '};' in line)
            
            map_start = map_lines[0]
            map_end = map_lines[map_end_index]
            map_lines = map_lines[1:map_end_index]

            import_lines.append(f'import {{ {comp_name}Component }} from \'./{widget_name}/{widget_name}.component\';\n')
        
            element_pattern = f'ElementType.{element_type}'
        
            if(not any(element_pattern in line for line in map_lines)):
                map_lines.append(f'    [{element_pattern}]: {comp_name}Component,\n')
            map_lines.append(f'    {comp_name}Component,\n')

            import_lines = uniq(import_lines)
            map_lines = uniq(map_lines)

            import_lines.sort()
            map_lines.sort()
                
            
            write_file(path, ''.join(import_lines) + '\n')
                
            write_file(path, ''.join(export_lines), 'a')
            
            write_file(path, ''.join([map_start] + map_lines + [map_end]), 'a')

@debuggable
def create_widget():
    """ Creates a new widget component

    Args:
        template_vals (dict):  The template values for the widget
    """    
    
    print(f'Creating widget: {GLOBALS.widget_name}')
    
    build_prime_templates()
    
    template_txt = search_replace(TEMPLATE, TEMPLATE_VALS)
    
    if(not GLOBALS.test_mode):
        print(utils.cmdx(f'ng g c {GLOBALS.widget_name}'))
    
    write_file(GLOBALS.WIDGET_COMP_PATH, template_txt)
    
    update_element_types()
    
    write_prime_templates()
        
    build_widget_config()
    
    update_index_file(GLOBALS.COMPS_INDEX)

# endregion Widget Functions
def main():
    get_template_vals()
    create_widget()
    
if(__name__ == '__main__'):
    main()