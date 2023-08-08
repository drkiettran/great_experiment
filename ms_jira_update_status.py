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
    return 'ms_jira_update_status'

def get_success_response(status):
    return {'ms_name': get_ms_name(), 'request_status': 'SUCCESS', 'payload': {'status': status}}

def get_failure_response(error):
    return {'ms_name': get_ms_name(), 'request_status': 'FAILURE', 'error': error}


# In[ ]:


class JIRA_Issue_Update_Status(BaseHTTPRequestHandler):
    global jira_handle
    def do_PUT(self):
        issue_id = self.path.split('/')[1]
        data_string = str(self.rfile.read(int(self.headers['Content-Length'])), 'utf-8')
        transition = json.loads(data_string)['status']
        logger.info(f'transitioning a jira issue for {issue_id} to {transition}')
        
        try:
            jira_issue = jira_handle.transition_issue(issue_id, transition=transition)
            response = get_success_response(transition)
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
    webserver = HTTPServer((server_name, server_port), JIRA_Issue_Update_Status)
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
        server_port = 8484
    
    jira_handle = None
    logger = None
    ms_init(os.environ['jira_url'], os.environ['jira_user_name'], os.environ['jira_user_psw'])
    start_webserver('localhost', server_port, logger)
    webserver.close()
    print("Server stopped.")


# In[ ]:


# JIRA experiment
logger = get_logger('TESTING')
jira_url = os.environ['jira_url']
jira_user_name = os.environ['jira_user_name']
jira_user_psw = os.environ['jira_user_psw']
print(jira_url, jira_user_name, jira_user_psw)
jira_handle = set_up_jira(logger, jira_url, jira_user_name, jira_user_psw)


# In[ ]:


issue_key = 'JRM-709'
jira_issue = jira_handle.issue(issue_key)
print('status:', jira_issue.fields.status.name)


# In[ ]:


jira_issue.update(notify=False, description="Quiet summary update.")


# In[ ]:


jira_issue.fields.labels = []
jira_issue.fields.labels.append("c:/dev/python/bdd/features/google_search.feature")
jira_issue.fields.labels.append("c:/dev/python/bdd/features/verify_logging_retention_period.feature")
jira_issue.update(fields={"labels": jira_issue.fields.labels})


# In[ ]:


dir(jira_handle)


# In[ ]:


jira_handle.transition_issue(issue_key, transition='Done')


# In[ ]:




