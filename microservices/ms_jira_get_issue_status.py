#!/usr/bin/env python
# coding: utf-8

# # Get status of a JIRA issue by issue_key

# In[ ]:


from http.server import BaseHTTPRequestHandler, HTTPServer
from jira import JIRA, exceptions
import os
import sys
import json
sys.path.append('.')
import utility


# In[ ]:


class Microservice(BaseHTTPRequestHandler):
    global app_log, app_jira_handle
    def get_success_response(self, payload):
        return {'ms_name': app_name, 'request_status': 'SUCCESS', 'payload': payload}

    def get_failure_response(self, error_code, error_text):
        return {'ms_name': app_name, 'request_status': 'FAILURE', 'error': {'error_code': error_code, 'error_text': error_text}}
        
    def do_GET(self):
        issue_id = self.path.replace('/','')
        app_log.info(f'getting jira issue status for {issue_id}')
        
        try:
            self.jira_issue = app_jira_handle.issue(issue_id)                        
            self.response_msg = self.get_success_response(self.jira_issue.fields.status.name)
        except exceptions.JIRAError as e:
            app_log.info(e.status_code)
            app_log.info(e.text)
            self.response_msg = self.get_failure_response(e.status_code, e.text)

        self.response()
        
    def response(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(self.response_msg),'utf-8'))


# In[ ]:


app_name = 'ms_jira_get_issue_status'
app_jira_handle = None
app_default_server_port = 8181
app_default_server_name = 'localhost'
app_log = utility.get_logger(app_name)
app_log.info(f'{app_name} starts ...')

if __name__ == "__main__":
    ## Required fixed parameters as hostname portnumber
    app_server_name, app_server_port = utility.get_server_info(app_default_server_name, app_default_server_port)
    app_log.info(f'Starting {app_server_name} at port {app_server_port}')
    app_jira_handle = utility.ms_init(app_name, app_log)
    utility.start_webserver(app_name, app_server_name, app_server_port, app_log, Microservice)


# In[ ]:




