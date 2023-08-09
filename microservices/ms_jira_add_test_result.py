#!/usr/bin/env python
# coding: utf-8

# # Add test result to a JIRA issue by issue id

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
        test_result = json.loads(str(self.rfile.read(int(self.headers['Content-Length'])), 'utf-8'))
        app_log.info(test_result['raw_text'])
        app_log.info(f'adding test result to a jira issue for {issue_id}')
        
        try:
            self.jira_issue = app_jira_handle.issue(issue_id)
            app_jira_handle.add_comment(issue_id, test_result['raw_text'])
            self.response_msg = self.get_success_response(test_result['raw_text'])
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


app_name = 'ms_jira_add_test_result'
app_jira_handle = None
app_default_server_port = 8787
app_default_server_name = 'localhost'
app_log = utility.get_logger(app_name)
app_log.info(f'{app_name} starts ...')

if __name__ == "__main__":
    ## Required fixed parameters as hostname portnumber
    app_server_name, app_server_port = utility.get_server_info(app_default_server_name, app_default_server_port)
    app_log.info(f'Starting {app_server_name} at port {app_server_port}')
    app_jira_handle = utility.ms_init(app_name, app_log)
    utility.start_webserver(app_name, app_server_name, app_server_port, app_log, Microservice)


# ```json
# {
#   "ms_name": "ms_jira_get_issue",
#   "request_status": "SUCCESS",
#   "payload": {
#     "expand": "renderedFields,names,schema,operations,editmeta,changelog,versionedRepresentations,customfield_10010.requestTypePractice",
#     "id": "10731",
#     "self": "https://drkiettran.atlassian.net/rest/api/2/issue/10731",
#     "key": "JRM-710",
#     "fields": {
#       "statuscategorychangedate": "2023-08-09T07:23:45.017-0400",
#       "issuetype": {
#         "self": "https://drkiettran.atlassian.net/rest/api/2/issuetype/10015",
#         "id": "10015",
#         "description": "Tasks track small, distinct pieces of work.",
#         "iconUrl": "https://drkiettran.atlassian.net/rest/api/2/universal_avatar/view/type/issuetype/avatar/10318?size=medium",
#         "name": "Task",
#         "subtask": false,
#         "avatarId": 10318,
#         "entityId": "0f2c3cb8-ef77-4674-8f5f-65281b393fa5",
#         "hierarchyLevel": 0
#       },
#       "timespent": null,
#       "customfield_10030": null,
#       "project": {
#         "self": "https://drkiettran.atlassian.net/rest/api/2/project/10003",
#         "id": "10003",
#         "key": "JRM",
#         "name": "jira-rmf-moderate",
#         "projectTypeKey": "software",
#         "simplified": true,
#         "avatarUrls": {
#           "48x48": "https://drkiettran.atlassian.net/rest/api/2/universal_avatar/view/type/project/avatar/10401",
#           "24x24": "https://drkiettran.atlassian.net/rest/api/2/universal_avatar/view/type/project/avatar/10401?size=small",
#           "16x16": "https://drkiettran.atlassian.net/rest/api/2/universal_avatar/view/type/project/avatar/10401?size=xsmall",
#           "32x32": "https://drkiettran.atlassian.net/rest/api/2/universal_avatar/view/type/project/avatar/10401?size=medium"
#         }
#       },
#       "fixVersions": [],
#       "customfield_10034": null,
#       "aggregatetimespent": null,
#       "customfield_10035": null,
#       "resolution": null,
#       "customfield_10036": null,
#       "customfield_10027": null,
#       "customfield_10028": null,
#       "customfield_10029": null,
#       "resolutiondate": null,
#       "workratio": -1,
#       "lastViewed": "2023-08-09T04:31:11.820-0400",
#       "issuerestriction": {
#         "issuerestrictions": {},
#         "shouldDisplay": true
#       },
#       "watches": {
#         "self": "https://drkiettran.atlassian.net/rest/api/2/issue/JRM-710/watchers",
#         "watchCount": 1,
#         "isWatching": true
#       },
#       "created": "2023-07-06T06:28:03.553-0400",
#       "customfield_10020": null,
#       "customfield_10021": null,
#       "customfield_10022": null,
#       "priority": {
#         "self": "https://drkiettran.atlassian.net/rest/api/2/priority/3",
#         "iconUrl": "https://drkiettran.atlassian.net/images/icons/priorities/medium.svg",
#         "name": "Medium",
#         "id": "3"
#       },
#       "customfield_10023": null,
#       "customfield_10024": null,
#       "customfield_10025": null,
#       "labels": [
#         "c:/dev/python/bdd/features/google_search.feature",
#         "c:/dev/python/bdd/features/verify_logging_retention_period.feature"
#       ],
#       "customfield_10026": null,
#       "customfield_10016": null,
#       "customfield_10017": null,
#       "customfield_10018": {
#         "hasEpicLinkFieldDependency": false,
#         "showField": false,
#         "nonEditableReason": {
#           "reason": "PLUGIN_LICENSE_ERROR",
#           "message": "The Parent Link is only available to Jira Premium users."
#         }
#       },
#       "customfield_10019": "0|i0009j:",
#       "timeestimate": null,
#       "aggregatetimeoriginalestimate": null,
#       "versions": [],
#       "issuelinks": [],
#       "assignee": null,
#       "updated": "2023-08-09T07:23:45.017-0400",
#       "status": {
#         "self": "https://drkiettran.atlassian.net/rest/api/2/status/10009",
#         "description": "",
#         "iconUrl": "https://drkiettran.atlassian.net/",
#         "name": "To Do",
#         "id": "10009",
#         "statusCategory": {
#           "self": "https://drkiettran.atlassian.net/rest/api/2/statuscategory/2",
#           "id": 2,
#           "key": "new",
#           "colorName": "blue-gray",
#           "name": "To Do"
#         }
#       },
#       "components": [],
#       "timeoriginalestimate": null,
#       "description": "a. Identify the types of events that the system is capable of logging in support of the audit function: [Assignment: organization-defined event types that the system is capable of logging];\nb. Coordinate the event logging function with other organizational entities requiring audit-related information to guide and inform the selection criteria for events to be logged;\nc. Specify the following event types for logging within the system: [Assignment: organization-defined event types (subset of the event types defined in AU-2a.) along with the frequency of (or situation requiring) logging for each identified event type];\nd. Provide a rationale for why the event types selected for logging are deemed to be adequate to support after-the-fact investigations of incidents; and\ne. Review and update the event types selected for logging [Assignment: organization-defined frequency].\n\n+*ACCEPTANCE CRITERIA*+:\n\n1) ...\n2) ...\n\n\n+*TEST SCENARIOS*+:\n{quote}{color:blue}+Scenario #1+{color}:\n\tGiven <the system is at state A>\n\tWhen <+this+ is done to the system>\n\tThen <the system should be at state A'>{quote}{quote}{color:blue}+Scenario #2+{color}:\n\tGiven <the system is at state A>\n\tWhen <+this+ is done to the system>\n\tThen <the system should be at state A'>{quote}",
#       "customfield_10010": null,
#       "customfield_10014": null,
#       "customfield_10015": null,
#       "timetracking": {},
#       "customfield_10005": null,
#       "customfield_10006": null,
#       "customfield_10007": null,
#       "security": null,
#       "customfield_10008": null,
#       "aggregatetimeestimate": null,
#       "attachment": [],
#       "customfield_10009": null,
#       "summary": "AU-2 EVENT LOGGING",
#       "creator": {
#         "self": "https://drkiettran.atlassian.net/rest/api/2/user?accountId=557058%3Add9cd837-885a-419a-aa72-02bd98d08f14",
#         "accountId": "557058:dd9cd837-885a-419a-aa72-02bd98d08f14",
#         "emailAddress": "drkiettran@gmail.com",
#         "avatarUrls": {
#           "48x48": "https://secure.gravatar.com/avatar/0e368ac36480d1e5797a9b1f4f20c716?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FKT-4.png",
#           "24x24": "https://secure.gravatar.com/avatar/0e368ac36480d1e5797a9b1f4f20c716?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FKT-4.png",
#           "16x16": "https://secure.gravatar.com/avatar/0e368ac36480d1e5797a9b1f4f20c716?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FKT-4.png",
#           "32x32": "https://secure.gravatar.com/avatar/0e368ac36480d1e5797a9b1f4f20c716?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FKT-4.png"
#         },
#         "displayName": "Kiet Tran",
#         "active": true,
#         "timeZone": "US/Eastern",
#         "accountType": "atlassian"
#       },
#       "subtasks": [],
#       "reporter": {
#         "self": "https://drkiettran.atlassian.net/rest/api/2/user?accountId=557058%3Add9cd837-885a-419a-aa72-02bd98d08f14",
#         "accountId": "557058:dd9cd837-885a-419a-aa72-02bd98d08f14",
#         "emailAddress": "drkiettran@gmail.com",
#         "avatarUrls": {
#           "48x48": "https://secure.gravatar.com/avatar/0e368ac36480d1e5797a9b1f4f20c716?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FKT-4.png",
#           "24x24": "https://secure.gravatar.com/avatar/0e368ac36480d1e5797a9b1f4f20c716?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FKT-4.png",
#           "16x16": "https://secure.gravatar.com/avatar/0e368ac36480d1e5797a9b1f4f20c716?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FKT-4.png",
#           "32x32": "https://secure.gravatar.com/avatar/0e368ac36480d1e5797a9b1f4f20c716?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FKT-4.png"
#         },
#         "displayName": "Kiet Tran",
#         "active": true,
#         "timeZone": "US/Eastern",
#         "accountType": "atlassian"
#       },
#       "aggregateprogress": {
#         "progress": 0,
#         "total": 0
#       },
#       "customfield_10001": null,
#       "customfield_10002": null,
#       "customfield_10003": null,
#       "customfield_10004": null,
#       "environment": null,
#       "duedate": null,
#       "progress": {
#         "progress": 0,
#         "total": 0
#       },
#       "comment": {
#         "comments": [
#           {
#             "self": "https://drkiettran.atlassian.net/rest/api/2/issue/10731/comment/11585",
#             "id": "11585",
#             "author": {
#               "self": "https://drkiettran.atlassian.net/rest/api/2/user?accountId=557058%3Add9cd837-885a-419a-aa72-02bd98d08f14",
#               "accountId": "557058:dd9cd837-885a-419a-aa72-02bd98d08f14",
#               "emailAddress": "drkiettran@gmail.com",
#               "avatarUrls": {
#                 "48x48": "https://secure.gravatar.com/avatar/0e368ac36480d1e5797a9b1f4f20c716?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FKT-4.png",
#                 "24x24": "https://secure.gravatar.com/avatar/0e368ac36480d1e5797a9b1f4f20c716?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FKT-4.png",
#                 "16x16": "https://secure.gravatar.com/avatar/0e368ac36480d1e5797a9b1f4f20c716?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FKT-4.png",
#                 "32x32": "https://secure.gravatar.com/avatar/0e368ac36480d1e5797a9b1f4f20c716?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FKT-4.png"
#               },
#               "displayName": "Kiet Tran",
#               "active": true,
#               "timeZone": "US/Eastern",
#               "accountType": "atlassian"
#             },
#             "body": "+*RELATED CONTROLS*+:\n\nAC-2 ACCOUNT MANAGEMENT\nAC-3 ACCESS ENFORCEMENT\nAC-6 LEAST PRIVILEGE\nAC-7 UNSUCCESSFUL LOGON ATTEMPTS\nAC-8 SYSTEM USE NOTIFICATION\nAC-16 SECURITY AND PRIVACY ATTRIBUTES\nAC-17 REMOTE ACCESS\nAU-3 CONTENT OF AUDIT RECORDS\nAU-4 AUDIT LOG STORAGE CAPACITY\nAU-5 RESPONSE TO AUDIT LOGGING PROCESS FAILURES\nAU-6 AUDIT RECORD REVIEW, ANALYSIS, AND REPORTING\nAU-7 AUDIT RECORD REDUCTION AND REPORT GENERATION\nAU-11 AUDIT RECORD RETENTION\nAU-12 AUDIT RECORD GENERATION\nCM-3 CONFIGURATION CHANGE CONTROL\nCM-5 ACCESS RESTRICTIONS FOR CHANGE\nCM-6 CONFIGURATION SETTINGS\nCM-13 DATA ACTION MAPPING\nIA-3 DEVICE IDENTIFICATION AND AUTHENTICATION\nMA-4 NONLOCAL MAINTENANCE\nMP-4 MEDIA STORAGE\nPE-3 PHYSICAL ACCESS CONTROL\nPM-21 ACCOUNTING OF DISCLOSURES\nPT-2 AUTHORITY TO PROCESS PERSONALLY IDENTIFIABLE INFORMATION\nPT-7 SPECIFIC CATEGORIES OF PERSONALLY IDENTIFIABLE INFORMATION\nRA-8 PRIVACY IMPACT ASSESSMENTS\nSA-8 SECURITY AND PRIVACY ENGINEERING PRINCIPLES\nSC-7 BOUNDARY PROTECTION\nSC-18 MOBILE CODE\nSI-3 MALICIOUS CODE PROTECTION\nSI-4 SYSTEM MONITORING\nSI-7 SOFTWARE, FIRMWARE, AND INFORMATION INTEGRITY\nSI-10 INFORMATION INPUT VALIDATION\nSI-11 ERROR HANDLING\n",
#             "updateAuthor": {
#               "self": "https://drkiettran.atlassian.net/rest/api/2/user?accountId=557058%3Add9cd837-885a-419a-aa72-02bd98d08f14",
#               "accountId": "557058:dd9cd837-885a-419a-aa72-02bd98d08f14",
#               "emailAddress": "drkiettran@gmail.com",
#               "avatarUrls": {
#                 "48x48": "https://secure.gravatar.com/avatar/0e368ac36480d1e5797a9b1f4f20c716?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FKT-4.png",
#                 "24x24": "https://secure.gravatar.com/avatar/0e368ac36480d1e5797a9b1f4f20c716?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FKT-4.png",
#                 "16x16": "https://secure.gravatar.com/avatar/0e368ac36480d1e5797a9b1f4f20c716?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FKT-4.png",
#                 "32x32": "https://secure.gravatar.com/avatar/0e368ac36480d1e5797a9b1f4f20c716?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FKT-4.png"
#               },
#               "displayName": "Kiet Tran",
#               "active": true,
#               "timeZone": "US/Eastern",
#               "accountType": "atlassian"
#             },
#             "created": "2023-07-06T06:28:04.282-0400",
#             "updated": "2023-07-06T06:28:04.282-0400",
#             "jsdPublic": true
#           },
#           {
#             "self": "https://drkiettran.atlassian.net/rest/api/2/issue/10731/comment/11586",
#             "id": "11586",
#             "author": {
#               "self": "https://drkiettran.atlassian.net/rest/api/2/user?accountId=557058%3Add9cd837-885a-419a-aa72-02bd98d08f14",
#               "accountId": "557058:dd9cd837-885a-419a-aa72-02bd98d08f14",
#               "emailAddress": "drkiettran@gmail.com",
#               "avatarUrls": {
#                 "48x48": "https://secure.gravatar.com/avatar/0e368ac36480d1e5797a9b1f4f20c716?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FKT-4.png",
#                 "24x24": "https://secure.gravatar.com/avatar/0e368ac36480d1e5797a9b1f4f20c716?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FKT-4.png",
#                 "16x16": "https://secure.gravatar.com/avatar/0e368ac36480d1e5797a9b1f4f20c716?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FKT-4.png",
#                 "32x32": "https://secure.gravatar.com/avatar/0e368ac36480d1e5797a9b1f4f20c716?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FKT-4.png"
#               },
#               "displayName": "Kiet Tran",
#               "active": true,
#               "timeZone": "US/Eastern",
#               "accountType": "atlassian"
#             },
#             "body": "+*DISCUSSION*+:\n\nAn event is an observable occurrence in a system. The types of events that require logging are those events that are significant and relevant to the security of systems and the privacy of individuals. Event logging also supports specific monitoring and auditing needs. Event types include password changes, failed logons or failed accesses related to systems, security or privacy attribute changes, administrative privilege usage, PIV credential usage, data action changes, query parameters, or external credential usage. In determining the set of event types that require logging, organizations consider the monitoring and auditing appropriate for each of the controls to be implemented. For completeness, event logging includes all protocols that are operational and supported by the system.\nTo balance monitoring and auditing requirements with other system needs, event logging requires identifying the subset of event types that are logged at a given point in time. For example, organizations may determine that systems need the capability to log every file access successful and unsuccessful, but not activate that capability except for specific circumstances due to the potential burden on system performance. The types of events that organizations desire to be logged may change. Reviewing and updating the set of logged events is necessary to help ensure that the events remain relevant and continue to support the needs of the organization. Organizations consider how the types of logging events can reveal information about individuals that may give rise to privacy risk and how best to mitigate such risks. For example, there is the potential to reveal personally identifiable information in the audit trail, especially if the logging event is based on patterns or time of usage.\nEvent logging requirements, including the need to log specific event types, may be referenced in other controls and control enhancements. These include AC-2(4), AC-3(10), AC-6(9), AC-17(1), CM-3f, CM-5(1), IA-3(3)(b), MA-4(1), MP-4(2), PE-3, PM-21, PT-7, RA-8, SC-7(9), SC-7(15), SI-3(8), SI-4(22), SI-7(8), and SI-10(1). Organizations include event types that are required by applicable laws, executive orders, directives, policies, regulations, standards, and guidelines. Audit records can be generated at various levels, including at the packet level as information traverses the network. Selecting the appropriate level of event logging is an important part of a monitoring and auditing capability and can identify the root causes of problems. When defining event types, organizations consider the logging necessary to cover related event types, such as the steps in distributed, transaction-based processes and the actions that occur in service-oriented architectures.",
#             "updateAuthor": {
#               "self": "https://drkiettran.atlassian.net/rest/api/2/user?accountId=557058%3Add9cd837-885a-419a-aa72-02bd98d08f14",
#               "accountId": "557058:dd9cd837-885a-419a-aa72-02bd98d08f14",
#               "emailAddress": "drkiettran@gmail.com",
#               "avatarUrls": {
#                 "48x48": "https://secure.gravatar.com/avatar/0e368ac36480d1e5797a9b1f4f20c716?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FKT-4.png",
#                 "24x24": "https://secure.gravatar.com/avatar/0e368ac36480d1e5797a9b1f4f20c716?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FKT-4.png",
#                 "16x16": "https://secure.gravatar.com/avatar/0e368ac36480d1e5797a9b1f4f20c716?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FKT-4.png",
#                 "32x32": "https://secure.gravatar.com/avatar/0e368ac36480d1e5797a9b1f4f20c716?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FKT-4.png"
#               },
#               "displayName": "Kiet Tran",
#               "active": true,
#               "timeZone": "US/Eastern",
#               "accountType": "atlassian"
#             },
#             "created": "2023-07-06T06:28:04.548-0400",
#             "updated": "2023-07-06T06:28:04.548-0400",
#             "jsdPublic": true
#           }
#         ],
#         "self": "https://drkiettran.atlassian.net/rest/api/2/issue/10731/comment",
#         "maxResults": 2,
#         "total": 2,
#         "startAt": 0
#       },
#       "votes": {
#         "self": "https://drkiettran.atlassian.net/rest/api/2/issue/JRM-710/votes",
#         "votes": 0,
#         "hasVoted": false
#       },
#       "worklog": {
#         "startAt": 0,
#         "maxResults": 20,
#         "total": 0,
#         "worklogs": []
#       }
#     }
#   }
# }
# 
# Click to add a cell.
# ```
