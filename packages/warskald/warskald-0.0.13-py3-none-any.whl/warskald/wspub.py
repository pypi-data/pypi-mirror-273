import os, json, sys, subprocess

WS_UI_PATH = '/home/joseph/coding_base/ws-ui-2'

def update_package_version(type: str = 'revision', path: str = WS_UI_PATH):
    print(f'Updating {type} increment of package version')
    
    with open(f'{path}/package.json', 'r') as reader:
        package = json.load(reader)
        reader.close()
    
    version_str = package.get('version','')
    version = version_str.split('.')
    
    print(f'Current version: {version_str}')
    
    if(type == 'revision'):
        version[2] = str(int(version[2]) + 1)
    elif(type == 'minor'):
        version[1] = str(int(version[1]) + 1)
        version[2] = '0'
    elif(type == 'major'):
        version[0] = str(int(version[0]) + 1)
        version[1] = '0'
        version[2] = '0'
        
    package['version'] = '.'.join(version)
    
    print(f'New version: {package["version"]}')
    
    print('Updating package.json file')
    
    with open(f'{path}/package.json', 'w') as writer:
        json.dump(package, writer, indent=2)
        writer.close()
        
    return package['version']

def list_find(items: list, value: str):
    for i, item in enumerate(items):
        if(item == value):
            return i
    return -1

def get_arg(arg: str | int):
    args = sys.argv
    if(isinstance(arg,str)):
        index = list_find(args, arg)
        if(index == -1):
            return None, -1
        return args[index], index
    elif(isinstance(arg,int)):
        if(arg < 0 or arg >= len(args)):
            return None, -1
        return args[arg], arg
    else:
        return None, -1
    
def build_lib():
    print('Building library')
    build_out = subprocess.run(['npm', 'run', 'build-lib'], capture_output=True).stdout.decode('utf-8')
    print(build_out)

def process_args():
    update_type, type_i = get_arg('--type')
    update_type = update_type if update_type else 'revision'
    
    has_message, msg_i = get_arg('--message')
    if(has_message):
        message = ' '.join(sys.argv[msg_i + 1:])
    else:
        message = None
    return update_type, message

def mprint(*args):
    print(*args, sep='\n')

def main():
    update_type, message = process_args()
    version = update_package_version(update_type)
    
    message = message if message else ''
    
    os.chdir(WS_UI_PATH)
    print('Updating git repository')
    
    status_out = subprocess.run(['git', 'status'], capture_output=True).stdout.decode('utf-8')
    mprint('git status', status_out)
    
    add_out = subprocess.run(['git', 'add', '.'], capture_output=True).stdout.decode('utf-8')
    mprint('git add .', add_out)
    
    commit_out = subprocess.run(['git', 'commit', '-m', f'Version updated to {version}\n{message}'], capture_output=True).stdout.decode('utf-8')
    mprint('git commit', commit_out)
    
    push_out = subprocess.run(['git', 'push'], capture_output=True).stdout.decode('utf-8')
    mprint('git push', push_out)
    
    dist_path = os.path.join(WS_UI_PATH, 'dist', 'warskald-ui')
    app_path = os.path.join(WS_UI_PATH, 'src', 'app')
    
    update_package_version(update_type, app_path)
    
    build_lib()
    
    os.chdir(dist_path)
    
    
    print('Publishing package to npm')
    pub_out = subprocess.run(['npm', 'publish', '--access', 'public'], capture_output=True).stdout.decode('utf-8')
    mprint('npm publish', pub_out)
    
    print('Process completed')
    
if(__name__ == '__main__'):
    main()