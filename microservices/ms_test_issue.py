#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import sys
import json
import subprocess
from urllib.parse import urlparse, parse_qs

sys.path.append('.')
import utility


# In[ ]:


class Microservice(BaseHTTPRequestHandler):
    # "c:/dev/python/bdd/features/google_search.feature"
    global app_log, app_jira_handle
    def proc_test_result(self, res_text):
        for line in res_text:
            if line.startswith('Failing scenario'):
                return False
            elif 'InvalidFileNameError' in line:
                return False
        return True

    def run_test(self):
        res = subprocess.run(["behave", self.test_scenario], capture_output=True) 
        res_text = str(res.stdout, 'UTF-8').replace('\r','').split('\n')
        test_result = {'result': self.proc_test_result(res_text), 'raw_text': "\n".join(res_text)}
        app_log.info(json.dumps(test_result, indent=4))
        return test_result
        
    def do_GET(self):
        test_scenario = self.path
        app_log.info(f'automated test for {test_scenario}')
        
        query_components = parse_qs(urlparse(self.path).query)
        app_log.info(query_components['test_scenario'][0])
        self.test_scenario = query_components["test_scenario"][0]
        self.response_msg = self.run_test()

        self.response()

    def response(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(self.response_msg),'utf-8'))


# In[ ]:


app_name = 'ms_test_issue'
app_jira_handle = None
app_default_server_port = 8383
app_default_server_name = 'localhost'
app_log = utility.get_logger(app_name)
app_log.info(f'{app_name} starts ...')

if __name__ == "__main__":
    ## Required fixed parameters as hostname portnumber
    app_server_name, app_server_port = utility.get_server_info(app_default_server_name, app_default_server_port)
    app_log.info(f'Starting {app_server_name} at port {app_server_port}')
    utility.start_webserver(app_name, app_server_name, app_server_port, app_log, Microservice)


# In[ ]:





# In[ ]:




