#encoding=utf8
#import magic_import
import sys
import os
import os.path
from flask import Flask
from flask import make_response, redirect, url_for, \
        send_from_directory, request, abort, after_this_request, request_started
import argparse
from gevent.wsgi import WSGIServer
import json
import ConfigParser
from jira import JIRA

app = Flask(__name__)

TO_DO = 'TO DO'
IN_PROGRESS = 'IN PROGRESS'
IN_PROGRESS_STORY = 'Start development'

@app.route('/',methods=["POST"])
def jira_status():
    '''
        当issue状态变成inprogress时检查被他block的story
        如果story数量为1, 检查story状态, 如果状态为todo
        将状态改成inprogress
    '''
    key = request.args.get('issue')
    jira = connect_jira()
    task = jira.issue(key)
    issuelinks = task.fields.issuelinks
    if len(issuelinks) == 1:
        story = issuelinks[0]
        story_key = story.raw.get('outwardIssue',{}).get('key')
        story = jira.issue(story_key)
        if story.fields.status.name == TO_DO:
            jira.transition_issue(story, transition= IN_PROGRESS_STORY)
            return 'succeed'
    return 'error'





def connect_jira():
    Config = ConfigParser.ConfigParser()
    Config.read('config')
    options = {
            'server': 'https://team.klook.com/jira'}
    jira = JIRA(options, basic_auth=(Config.get('User', 'user_name'), Config.get('User', 'password')))
    return jira


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
