#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import logging
import sys
import json
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from urllib.parse import urlparse, parse_qs
#from urlparse import urlparse, parse_qs


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


def proc_test_result(res_text):
    for line in res_text:
        if line.startswith('Failing scenario'):
            return False
    return True

def run_test(test_scenario):
    res = subprocess.run(["behave", test_scenario ], capture_output=True) 
    res_text = str(res.stdout, 'UTF-8').replace('\r','').split('\n')
    test_result = {'result': proc_test_result(res_text), 'raw_text': "\n".join(res_text)}
    print(json.dumps(test_result, indent=4))
    return test_result

def get_ms_name():
    return 'ms_test_issue'


# In[ ]:


class Test_Automation(BaseHTTPRequestHandler):
    # "c:\\dev\\python\\bdd\\features\\google_search.feature"
    def do_GET(self):
        test_scenario = self.path
        
        logger.info(f'automated test for {test_scenario}')
        
        query_components = parse_qs(urlparse(self.path).query)
        logger.info(query_components['test_scenario'][0])
        test_scenario = query_components["test_scenario"][0]
        response = run_test(test_scenario)
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(response),'utf-8'))


# In[ ]:


def start_webserver(server_name, server_port, log):
    webserver = HTTPServer((server_name, server_port), Test_Automation)
    log.info("%s started http://%s:%s" % (get_ms_name(), server_name, server_port))

    try:
        webserver.serve_forever()
    except KeyboardInterrupt:
        print("Interrupted by keyboard ...")


# In[ ]:


def ms_init():
    global logger
    logger = get_logger(get_ms_name())

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1].isnumeric():
        server_port = int(sys.argv[1])
    else:
        server_port = 8383
    
    logger = None
    ms_init()
    start_webserver('localhost', server_port, logger)
    webserver.close()
    print("Server stopped.")


# In[ ]:





# In[ ]:




