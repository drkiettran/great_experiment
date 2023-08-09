#!/usr/bin/env python
# coding: utf-8

# In[ ]:


## https://jira.readthedocs.io/examples.html
    
from jira import JIRA, exceptions
import logging
import sys, os
import json
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from urllib.parse import urlparse, parse_qs


# In[ ]:


def get_logger(logger_name):    
    log = logging.getLogger(logger_name)
    log.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    log.handlers = [handler]
    return log


# In[ ]:


def init_jira_environment(log, jira_url, user_name, user_psw):
    jira_options = {'server': jira_url}
    log.info(f"server: {jira_options['server']}")
    jira_handle = JIRA(options=jira_options, basic_auth=(user_name, user_psw))
    return jira_handle

def get_ms_name():
    return 'ms_jira_get_test_scenarios'

def get_success_response(test_scenarios):
    return {'ms_name': get_ms_name(), 'request_status': 'SUCCESS', 'payload': {'test_scenarios': test_scenarios}}

def get_failure_response(error):
    return {'ms_name': get_ms_name(), 'request_status': 'FAILURE', 'error': error}


# In[ ]:


class JIRA_Get_Test_Scenarios(BaseHTTPRequestHandler):
    global jira_handle
    def do_GET(self):
        issue_id = self.path.split('/')[1]
        logger.info(f'getting test scenarios for issue {issue_id}')
        
        try:
            jira_issue = jira_handle.issue(issue_id)
            response = get_success_response(jira_issue.fields.labels)
        except exceptions.JIRAError as e:
            logger.info(e.status_code)
            logger.info(e.text)
            response = get_failure_response(e.status_code)
                    
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(response),'utf-8'))


# In[ ]:


def start_webserver(server_name, server_port, log):
    webserver = HTTPServer((server_name, server_port), JIRA_Get_Test_Scenarios)
    log.info("%s started http://%s:%s" % (get_ms_name(), server_name, server_port))

    try:
        webserver.serve_forever()
    except KeyboardInterrupt:
        print("Interrupted by keyboard ...")

def set_up_jira(logger, jira_url, user_name, user_psw):
    return init_jira_environment(logger, jira_url, user_name, user_psw)


# In[ ]:


def ms_init(jira_url, user_name, user_psw):
    global logger, jira_handle
    logger = get_logger(get_ms_name())
    jira_handle = set_up_jira(logger, jira_url, user_name, user_psw)
    print (jira_handle)
    
if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1].isnumeric():
        server_port = int(sys.argv[1])
    else:
        server_port = 8585
    
    jira_handle = None
    logger = None
    ms_init(os.environ['jira_url'], os.environ['jira_user_name'], os.environ['jira_user_psw'])
    start_webserver('localhost', server_port, logger)
    webserver.close()
    print("Server stopped.")


# In[ ]:





# In[ ]:




