import os, json, subprocess
from ._globals import GLOBALS


def get_ports() -> dict:
    
    with open(GLOBALS.PORTS_FILE, 'r') as reader:
        ports = json.load(reader)
        reader.close()
    return ports

def get_port(path: str) -> int:
        
    ports = get_ports()
    
    port = ports.get(path)
    if(port is None):
        max_port = max(ports.values()) if len(ports) > 0 else None
        port = max_port + 1 if max_port is not None else 4200
        
    return port

def save_ports(ports: dict) -> None:
    with open(GLOBALS.PORTS_FILE, 'w') as writer:
        json.dump(ports, writer)
        writer.close()
        
def main():
        
    path = os.getcwd()
    port = get_port(path)
    
    ports = get_ports()
    ports[path] = port
    save_ports(ports)
    
    subprocess.run(['ng', 'serve', '--port', str(port)])
    
if(__name__ == '__main__'):
    main()