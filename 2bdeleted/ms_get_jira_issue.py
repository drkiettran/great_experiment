#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from jira import JIRA, exceptions
import logging
import sys
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import time


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
    return 'ms_get_jira_issue'

def get_success_response(payload):
    return {'ms_name': get_ms_name(), 'request_status': 'SUCCESS', 'payload': payload}

def get_failure_response(error):
    return {'ms_name': get_ms_name(), 'request_status': 'FAILURE', 'error': error}


# In[ ]:


class JIRA_Issue(BaseHTTPRequestHandler):
    global jira_handle
    def do_GET(self):
        issue_id = self.path
        logger.info(f'getting jira issue for {issue_id}')
        
        try:
            jira_issue = jira_handle.issue(issue_id)                        
            response = get_success_response(jira_issue.raw)
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
    webserver = HTTPServer((server_name, server_port), JIRA_Issue)
    log.info("%s started http://%s:%s" % (get_ms_name(), server_name, server_port))

    try:
        webserver.serve_forever()
    except KeyboardInterrupt:
        print("Interrupted by keyboard ...")

def set_up_jira(logger, jira_url, user_name, user_psw):
    return init_jira_environment(logger, jira_url, user_name, user_psw)


# In[ ]:


## Main program


# In[ ]:


def ms_init():
    global logger, jira_handle
    logger = get_logger('MBSEAX')
    user_name = "drkiettran@gmail.com"
    user_psw  = "ATATT3xFfGF0CpUUGjus2XI6C7XkOJM01D0AiuJzJQOwgOjbmfLyRhYecFraMtNHyVqrbfMbKgtHrQ4J6mHFM9CMONhJTbImC5T0lEW7h5SUXD6lBcCkq-jeaZEhrBfiXdmwpeBF82mOcrtUUPcXaiLwj_2RpjFeOpIzcqJNrq5yP7Aq5eoYZ08=89250AFC"
    jira_handle = set_up_jira(logger, 'https://drkiettran.atlassian.net', user_name, user_psw)
    print (jira_handle)
    
if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1].isnumeric():
        server_port = int(sys.argv[1])
    else:
        server_port = 8080
    
    jira_handle = None
    logger = None
    ms_init()
    start_webserver('localhost', server_port, logger)
    webserver.close()
    print("Server stopped.")
    


# In[ ]:




