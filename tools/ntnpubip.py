from flask import request

def pubip():

    return(request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
