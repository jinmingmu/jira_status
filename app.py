#encoding=utf8
#import magic_import
import sys
import os
import os.path
from flask import Flask
from flask import make_response, redirect, url_for, \
        send_from_directory, request, abort, after_this_request
import argparse
from gevent.wsgi import WSGIServer

app = Flask(__name__)

@app.route('/',methods=["GET"])
def jira_status():
    '''
       得到jira的post请求数据 
    '''
    return 'lala'


def run(port):
    http_server = WSGIServer(('0.0.0.0', port), app)
    http_server.serve_forever()
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-port', help='the port of app list  on, default 9527', default=9527, type=int)
    args = parser.parse_args()
    run(args.port)

if __name__ == '__main__':
    main()
