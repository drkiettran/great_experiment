from jira import JIRA, exceptions
import logging
import sys
import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

def get_logger(logger_name):    
    log = logging.getLogger(logger_name)
    log.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    log.handlers = [handler]
    return log

def init_jira_environment(log, jira_url, user_name, user_psw):
    jira_options = {'server': jira_url}
    log.info(f"server: {jira_options['server']}")
    jira_handle = JIRA(options=jira_options, basic_auth=(user_name, user_psw))
    return jira_handle

def start_webserver(app_name, server_name, server_port, log, class_name):
    webserver = HTTPServer((server_name, server_port), class_name)
    log.info("%s started http://%s:%s" % (app_name, server_name, server_port))

    try:
        webserver.serve_forever()
    except KeyboardInterrupt:
        print("Interrupted by keyboard ...")

def set_up_jira(log, jira_url, user_name, user_psw):
    return init_jira_environment(log, jira_url, user_name, user_psw)

def ms_init(ms_name, log):
    jira_url = os.environ['jira_url']
    jira_user_name = os.environ['jira_user_name']
    jira_user_psw = os.environ['jira_user_psw']
    log.info(f'initializing {ms_name} with url: {jira_url}, user name: {jira_user_name}, token: {jira_user_psw} ...')
    return set_up_jira(log, jira_url, jira_user_name, jira_user_psw)
    
def get_server_info(default_server_name, default_server_port):
    if 'ipykernel_launcher' in sys.argv[0]:
        return default_server_name, default_server_port
    elif len(sys.argv) == 3:
        return sys.argv[1], int(sys.argv[2])
    else:
        print('Required server_name and server_port ... Exit.')
        sys.exit(-1)