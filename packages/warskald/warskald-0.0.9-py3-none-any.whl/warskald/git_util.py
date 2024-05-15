import os, json, subprocess, sys

def exec(cmd: list[str]) -> str:
    process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process.stdout.decode('utf-8')

def get_branch():
    cmd = ['git', 'rev-parse', '--abbrev-ref', 'HEAD']
    return exec(cmd).strip()

def check_branch_in_remote(branch: str):
    cmd = ['git', 'ls-remote', '--heads', 'origin', branch]
    return exec(cmd).strip() != ''

def git_add(file: str = '.'):
    print('Adding files to git\n')
    cmd = ['git', 'add', file]
    return exec(cmd)

def git_commit(message: str):
    print('Committing files to git\n')
    cmd = ['git', 'commit', '-m', message]
    return exec(cmd)

def git_push(branch: str):
    print('Pushing files to git\n')
    if(check_branch_in_remote(branch)):
        print(f'{branch} exists in remote, pushing')
        cmd = ['git', 'push']
        return exec(cmd)
    else:
        print(f'{branch} does not exist in remote, creating remote branch')
        cmd = ['git', 'push', '-u', 'origin', branch]
        return exec(cmd)

def parse_args() -> dict:
    # TODO: make this work later when I care
    parsed_args = {}
    args = sys.argv[1:]
    for i, arg in enumerate(args):
        if arg.startswith('--'):
            key = arg[2:]
            if(i+1 < len(args) and not args[i+1].startswith('--')):
                value = args[i+1]
            parsed_args[key] = value
    return parsed_args

def main():
    branch = get_branch()
    message = ' '.join(sys.argv[1:])
    if(not message):
        message = 'Automated commit'
    print(f'Branch: {branch}')
    print(f'Message: {message}')
    
    print(git_add())
    
    print(git_commit(message))
    
    print(git_push(branch))
    
if( __name__ == '__main__'):
    main()