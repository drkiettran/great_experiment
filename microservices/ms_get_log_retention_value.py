#!/usr/bin/env python
# coding: utf-8

# # get log retention value (in days)
# 
# **Request**:
# ```
# POST / HTTP/1.1
# Host: logs.<region>.<domain>
# X-Amz-Date: <DATE>
# Authorization: AWS4-HMAC-SHA256 Credential=<Credential>, SignedHeaders=content-type;date;host;user-agent;x-amz-date;x-amz-target;x-amzn-requestid, Signature=<Signature>
# User-Agent: <UserAgentString>
# Accept: application/json
# Content-Type: application/x-amz-json-1.1
# Content-Length: <PayloadSizeBytes>
# Connection: Keep-Alive
# X-Amz-Target: Logs_20140328.Describe
# ```
# **Response**:
# ```
# HTTP/1.1 200 OK
# x-amzn-RequestId: <RequestId>
# Content-Type: application/x-amz-json-1.1
# Content-Length: <PayloadSizeBytes>
# Date: <Date>
# {
#   "logGroups": [
#     {
#       "storageBytes": 1048576,
#       "arn": "arn:aws:logs:us-east-1:123456789012:log-group:my-log-group-1:*",
#       "creationTime": 1393545600000,
#       "logGroupName": "my-log-group-1",
#       "metricFilterCount": 0,
#       "retentionInDays": 14,
#       "kmsKeyId": "arn:aws:kms:us-east-1:123456789012:key/abcd1234-a123-456a-a12b-a123b4cd56ef"
#     },
#     {
#       "storageBytes": 5242880,
#       "arn": "arn:aws:logs:us-east-1:123456789012:log-group:my-log-group-2:*",
#       "creationTime": 1396224000000,
#       "logGroupName": "my-log-group-2",
#       "metricFilterCount": 0,
#       "retentionInDays": 30
#     }
#   ]
# }
# ```LogGroups

# # Python example with JSON request/response
# 
# **reference**: 
# - `https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_DescribeLogGroups.html`
# - `https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_log_groups.html#`
# 
# **Request**:
# ```python
# response = client.describe_log_groups(
#     accountIdentifiers[  'strin]  ],
#     logGroupNamePrefix='string',
#     logGroupNamePattern='string',
#     nextToken='string',
#     limit=123,
#     includeLinkedAccounts=True
# ```
# **Response**:
# ```json
# {
#     'logGroups': [
#         {
#             'logGroupName': 'string',
#             'creationTime': 123,
#             'retentionInDays': 123,
#             'metricFilterCount': 123,
#             'arn': 'string',
#             'storedBytes': 123,
#             'kmsKeyId': 'string',
#             'dataProtectionStatus': 'ACTIVATED'|'DELETED'|'ARCHIVED'|'DISABLED',
#             'inheritedProperties': [
#                 'ACCOUNT_DATA_PROTECTION',
#             ]
#         },
#     ],
#     'nextToken': 'string'
# }
# ```
# |False
# )

# In[ ]:


from http.server import BaseHTTPRequestHandler, HTTPServer
from jira import JIRA, exceptions
import os
import sys
import json
sys.path.append('.')
import utility


# In[ ]:





# In[ ]:


class Microservice(BaseHTTPRequestHandler):
    global app_log, app_jira_handle
    def get_success_response(self, payload):
        return {'ms_name': app_name, 'request_status': 'SUCCESS', 'payload': payload}

    def get_failure_response(self, error):
        return {'ms_name': app_name, 'request_status': 'FAILURE', 'error': error}

    def get_retention_value(self, log_group_name):
        with open('./log_groups_response.json') as reader: # Replace this with a boto3 call to AWS.
            log_group_info = json.load(reader)
        app_log.info(json.dumps(log_group_info, indent=2))
        for log_group in log_group_info['logGroups']:
            if log_group['logGroupName'] == log_group_name:
                return int(log_group['retentionInDays'])
        return -1 # not found
        
    def do_GET(self):        
        log_group_name = self.path.replace('/','')
        app_log.info(f'getting logging retention value for {log_group_name}')
        
        try:
            retention_value = self.get_retention_value(log_group_name)
            #jira_issue = app_jira_handle.issue('JRM-710')  # example/testing ... to be removed for this module.
            if retention_value > 0:
                self.response_msg = self.get_success_response(retention_value)
            else:
                self.response_msg = self.get_failure_response(f'log group {log_group_name} is not found!')
        except exceptions.JIRAError as e:
            app_log.info(e.status_code)
            app_log.info(e.text)
            self.response_msg = self.get_failure_response(e.status_code)
        self.response()
        
    def response(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(self.response_msg),'utf-8'))
        


# In[ ]:


app_name = 'ms_get_logging_rentention_value'
app_jira_handle = None
app_default_server_port = 8686
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




