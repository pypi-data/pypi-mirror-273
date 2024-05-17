import os, sys
from caseconverter import camelcase

def main():
    if(len(sys.argv) < 2):
        print('Usage: python run_ngwidget.py widget-name')
        return
    widget_name = sys.argv[1]
    prime_name = camelcase(widget_name)
    cmd = f'python3.11 /home/joseph/coding_base/scripts/utils/ngwidget.py -n {widget_name} -p {prime_name} -f -r'
    if(len(sys.argv) > 2):
        cmd += ' -T -d'
        
    os.system(cmd)
    
if(__name__ == '__main__'):
    main()