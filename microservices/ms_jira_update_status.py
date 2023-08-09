#!/usr/bin/env python
# coding: utf-8

# # Update status of a JIRA issue by issue id

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
 
    def do_PUT(self):
        issue_id = self.path.replace('/','')
        data_string = str(self.rfile.read(int(self.headers['Content-Length'])), 'utf-8')
        transition = json.loads(data_string)['status']
        app_log.info(f'transitioning a jira issue for {issue_id} to {transition}')
        
        try:
            self.jira_issue = app_jira_handle.transition_issue(issue_id, transition=transition)
            self.response_msg = self.get_success_response(transition)
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


app_name = 'ms_jira_update_status'
app_jira_handle = None
app_default_server_port = 8585
app_default_server_name = 'localhost'
app_log = utility.get_logger(app_name)
app_log.info(f'{app_name} starts ...')

if __name__ == "__main__":
    ## Required fixed parameters as hostname portnumber
    app_server_name, app_server_port = utility.get_server_info(app_default_server_name, app_default_server_port)
    app_log.info(f'Starting {app_server_name} at port {app_server_port}')
    app_jira_handle = utility.ms_init(app_name, app_log)
    utility.start_webserver(app_name, app_server_name, app_server_port, app_log, Microservice)


# # NOTE (DON'T DELETE)

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




