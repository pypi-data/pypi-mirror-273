from flask import request, g, has_request_context
from warskald.utils import parse_str_type

def parse_request_data():
    if(has_request_context() and request):
        g.request_data = {}
        
        if(request.method == 'GET'):
            for key, value in request.args.items():
                g.request_data[key] = parse_str_type(value)
        else:    
            g.request_data = request.get_json()
            
        return g.request_data