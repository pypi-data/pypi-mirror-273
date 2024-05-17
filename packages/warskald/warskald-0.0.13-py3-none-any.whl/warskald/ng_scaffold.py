from __future__ import annotations
import os, re, json, sys, subprocess, shutil
from tqdm import tqdm

# region Constants

APP_ROOT = 'src/app'
UTIL_DIR = sys.argv[0].replace('ng_scaffold.py', '')
NG_FILES = os.path.join(UTIL_DIR, 'ng_files')
DIRS = [
    'components',
    'common',
    'models',
    'pages',
    'services',
]

NPM_PACKAGES = {
    'dependencies': [
        'primeng',
        'primeicons',
        'primeflex',
        'lodash',
        'nanoid',
        'font-awesome',
        'ngx-bootstrap',
        'ngx-device-detector',
        'bootstrap',
    ],
    'devDependencies': [
        'eslint',
        '@typescript-eslint/eslint-plugin',
        '@types/lodash',
    ]
}

NG_NEW_OPTION_SETS = {
    'default': [
        '--routing',
        'true',
        '--style',
        'scss',
        '--standalone',
        'false',
        '--skip-tests',
        'true',
        '--ssr',
        'false',
    ],
    'standalone': [
        '--routing',
        'true',
        '--style',
        'scss',
        '--standalone',
        'true',
        '--skip-tests',
        'true',
        '--ssr',
        'false',
    ],
    'default-no-routing': [
        '--routing',
        'false',
        '--style',
        'scss',
        '--standalone',
        'false',
        '--skip-tests',
        'true',
        '--ssr',
        'false',
    ],
    'standalone-no-routing': [
        '--routing',
        'false',
        '--style',
        'scss',
        '--standalone',
        'true',
        '--skip-tests',
        'true',
        '--ssr',
        'false',
    ],
    'ssr-default': [
        '--routing',
        'true',
        '--style',
        'scss',
        '--standalone',
        'false',
        '--ssr',
        'true',
        '--skip-tests',
        'true',
    ],
    'ssr-no-routing': [
        '--routing',
        'false',
        '--style',
        'scss',
        '--standalone',
        'false',
        '--ssr',
        'true',
        '--skip-tests',
        'true',
    ],
    'ssr-standalone': [
        '--routing',
        'true',
        '--style',
        'scss',
        '--standalone',
        'true',
        '--ssr',
        'true',
        '--skip-tests',
        'true',
    ],
    'ssr-standalone-no-routing': [
        '--routing',
        'false',
        '--style',
        'scss',
        '--standalone',
        'true',
        '--ssr',
        'true',
        '--skip-tests',
        'true',
    ],
}

COMPONENT_FILE_REGEX = r'^.*\.component\.(ts)$'
# endregion Constants


# region Util Functions

def get_installed_packages() -> list[str]:
    result = subprocess.run(['npm', 'list'], capture_output=True, text=True)
    return list(filter(lambda x: x != '', [ item.split('@')[0].replace('├── ','').replace('└── ','') for item in result.stdout.split('\n') ]))
        
def copy_file(src_dir: str, file_name: str, dest: str):
    src_path = os.path.join(src_dir, file_name)
    dest_path = os.path.join(dest, file_name)
    if(os.path.exists(src_path)):
        if(file_name not in os.listdir(dest)):
            print(f'Copying {file_name}')
            shutil.copyfile(src_path, dest_path)
        else:
            print(f'File already exists: {dest_path}')
    else:
        print(f'Source file not found: {src_path}')
           
def create_dir(_dir: str, src_path: str = None, dest_path: str = None):
    
    if(src_path is None):
        base_path = os.path.join(NG_FILES, _dir)
    else:
        base_path = src_path
        
    if(dest_path is None):
        app_path = os.path.join(APP_ROOT, _dir)
    else:
        app_path = dest_path
        
    print(f'\ndir: {_dir}\nbase_path: {base_path}\napp_path: {app_path}')
    
    if(not os.path.exists(app_path)):
        print(f'Creating directory: {app_path}')
        os.makedirs(app_path)
    else:
        print(f'Directory already exists: {app_path}')
        
    if(os.path.exists(base_path) and os.path.exists(app_path)):
        dir_items = os.listdir(base_path)
        
        print(f'Copying items from {base_path} to {app_path}')
        
        for dir_item in tqdm(dir_items):
            item_base_path = os.path.join(base_path, dir_item)
            item_app_path = os.path.join(app_path, dir_item)
            print(f'\nitem_base_path: {item_base_path}\nitem_app_path: {item_app_path}')
            if(os.path.exists(item_base_path)):
                if(os.path.isdir(item_base_path)):
                    if(dir_item not in os.listdir(app_path)):
                        print(f'Creating directory: {item_app_path}')
                        os.makedirs(item_app_path)
                    else:
                        print(f'Directory already exists: {item_app_path}')
                    create_dir(dir_item, item_base_path, item_app_path)
                else:
                    copy_file(base_path, dir_item, app_path)
        
    if('_index.ts' not in os.listdir(app_path)):
        print(f'Creating _index.ts and placeholder in {app_path}')
        
        with open(os.path.join(app_path, '_index.ts'), 'w') as file:
            file.write('export * from \'./placeholder\'')
        with open(os.path.join(app_path, 'placeholder.ts'), 'w') as file:
            file.write('export const placeholder = \'placeholder\'')
            
    """ base_services_path = os.path.join(NG_FILES, 'services')
    base_models_path = os.path.join(NG_FILES, 'models')
    app_services_path = os.path.join(APP_ROOT, 'services')
    app_models_path = os.path.join(APP_ROOT, 'models')
    
    service_files = os.listdir(base_services_path)
    model_files = os.listdir(base_models_path)
    
    for _dir in DIRS:
        if(_dir in os.listdir(NG_FILES)):
            pass
    
    print(f'Copying files to {app_services_path}')
    for file in tqdm(service_files):
        copy_file(base_services_path, file, app_services_path)
                
    print(f'Copying files to {app_models_path}')
    for file in tqdm(model_files):
        copy_file(base_models_path, file, app_models_path) """

def find_arg(arg: str):
    args = sys.argv
    try:
        arg_index = args.index(arg)
        return args[arg_index], arg_index
    except ValueError:
        return None, -1
    except Exception as e:
        print(f'Error finding arg: {arg}')
        print(e)
        return None, -1

def get_arg(index: int, default: str = None) -> str:
    args = sys.argv
    if(len(args) > index):
        return args[index]
    return default

def clean_json(target: str = 'tsconfig.json'):
    
    if(not os.path.exists(target)):
        print(f'{target} not found')
        
    with open(target, 'r') as reader:
        lines = reader.readlines()
        clean_lines = [ line for line in lines if not re.match(r'^\s*\/[\*|\/]', line) ]
        
    with open(target, 'w') as writer:
        writer.writelines(clean_lines)

def get_packages(target: str) -> dict[str, list[str]]:
    package_json_path = os.path.join(target, 'package.json')
    if(not os.path.exists(package_json_path)):
        print(f'package.json not found in {target}')
        return []
    
    clean_json(package_json_path)
    
    packages = NPM_PACKAGES.copy()
    existing = packages.get('dependencies', []) + packages.get('devDependencies', [])
    with open(package_json_path, 'r') as file:
        package_json = json.load(file)
        packages['dependencies'].extend([ package for package in list(package_json.get('dependencies', {}).keys()) if package not in existing])
        packages['devDependencies'].extend([ package for package in list(package_json.get('devDependencies', {}).keys()) if package not in existing])
    return packages
# endregion Util Functions


# region Main Functions

def npm_install(packages: dict[str, list[str]] = NPM_PACKAGES):
    existing = get_installed_packages()
    
    for package in tqdm(packages.get('dependencies', [])):
        if(package not in existing):
            subprocess.run(['npm', 'install', package])
        else:
            print(f'Package already installed: {package}')
            
    for package in tqdm(packages.get('devDependencies', [])):
        if(package not in existing):
            subprocess.run(['npm', 'install', '--save-dev', package])
        else:
            print(f'Package already installed: {package}')

def create_dirs():
    for _dir in tqdm(DIRS):
        
        create_dir(_dir)
        
def copy_eslintrc():
    src_path = os.path.join(NG_FILES, '.eslintrc.json')
    dest_path = '.eslintrc.json'
    if(os.path.exists(src_path)):
        if('eslintrc.json' not in os.listdir()):
            print(f'Copying eslintrc.json')
            shutil.copyfile(src_path, dest_path)
        else:
            print(f'File already exists: {dest_path}')
    else:
        print(f'Source file not found: {src_path}')
   
def update_tsconfig():
    clean_json()
    tsconfig_path = 'tsconfig.json'
    if(not os.path.exists(tsconfig_path)):
        print('tsconfig.json not found')
    with open(tsconfig_path, 'r') as file:
        tsconfig = json.load(file)
        tsconfig['compilerOptions']['baseUrl'] = './'
        tsconfig['compilerOptions']['noPropertyAccessFromIndexSignature'] = False
        tsconfig['compilerOptions']['noUnusedLocals'] = False
        tsconfig['compilerOptions']['noUnusedParameters'] = False
        tsconfig['compilerOptions']['allowSyntheticDefaultImports'] = True
        paths = {}
        for _dir in DIRS:
            paths[f'@{_dir}'] = [f'{APP_ROOT}/{_dir}/_index.ts']
        tsconfig['compilerOptions']['paths'] = paths
        
    with open(tsconfig_path, 'w') as file:
        json.dump(tsconfig, file, indent=4)
        
def cd(target: str):
    if(target is None):
        print('Target directory required')
        return
    
    if(not os.path.exists(target)):
        print(f'Target directory not found: {target}')
        return
    
    os.chdir(target)
    print(f'Current directory: {os.getcwd()}')

def copy_app(target_dir: str):
    if(target_dir is None):
        print('Target directory required')
        return
    
    if(not os.path.exists(target_dir)):
        print(f'Target directory not found: {target_dir}')
        return
    
    src_dir = os.path.join(target_dir, 'src')
    
    packages = get_packages(target_dir)
    
    print(f'Installing packages in {target_dir}')
    npm_install(packages)
    
    """ cd('src')
    copy_assets = os.path.join(src_dir, 'assets')
    target_assets = os.path.join(os.getcwd(), 'assets')
    print(f'Copying assets from {copy_assets} to {target_assets}')
    shutil.copytree(copy_assets, target_assets, dirs_exist_ok=True)
    
    cd('app') """
    
    
    
            
    

def process_args():
    npm, npm_i = find_arg('npm')
    dirs, dirs_i = find_arg('create_dirs')
    tsconfig, tsconfig_i = find_arg('tsconfig')
    eslintrc, eslintrc_i = find_arg('eslintrc')
    new_app, new_app_i = find_arg('new')
    all_functs, all_functs_i = find_arg('all')
    copy_content, copy_content_i = find_arg('copy_content')
    copy_target = get_arg(copy_content_i + 1) if copy_content else None
    if(copy_target):
        copy_target = os.path.abspath(copy_target) 
            
    if(new_app):
        app_name = get_arg(new_app_i + 1)
        if(app_name is None):
            print('App name required')
            return
        if(app_name in os.listdir()):
            print(f'App already exists: {app_name}')
            return
        if('angular.json' in os.listdir()):
            print('Cannot create new app in existing angular project')
            return
        ng_new_option_set, ng_new_i = find_arg('option_set')
        if(ng_new_option_set):
            ng_new_option_set = get_arg(ng_new_i + 1)
        else:
            ng_new_option_set = 'standalone'
        
        ng_new_options: list[str] = NG_NEW_OPTION_SETS.get(ng_new_option_set, NG_NEW_OPTION_SETS['standalone'])
        
        cmd = ['ng', 'new', app_name] + ng_new_options
        cmd_str = ' '.join(cmd)
        print(f'Executing: {cmd_str}')
        
        subprocess.run(cmd)
        print(f'Changing directory to {app_name}')
        os.chdir(app_name)
        print(f'current directory: {os.getcwd()}')
    
    if('angular.json' not in os.listdir()):
        print('Execute in root angular directory')
        return
    
    if(get_arg(0) is None or all_functs):
        create_dirs()
        npm_install()
        update_tsconfig()
        copy_eslintrc()
    else:
        if(dirs):
            create_dirs()
        if(npm):
            npm_install()
        if(tsconfig):
            update_tsconfig()
        if(eslintrc):
            copy_eslintrc()
        if(copy_content):
            target = get_arg(copy_content_i + 1)
            copy_app(copy_target)
            
            
# endregion Main Functions
    
            
def main():
    
    process_args()
    

if __name__ == "__main__":
    main()