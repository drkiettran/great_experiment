from behave   import given, when, then
from hamcrest import assert_that, equal_to, greater_than
import json
import os

expected_log_group_name = None
log_group_policy = None

@given(u'I have a log group "{log_group_name}" retention policy')
def step_impl(context, log_group_name):
    global expected_log_group_name
    expected_log_group_name = log_group_name


@when(u'I retrieve the rention policy')
def step_impl(context):
    global log_group_policy
    log_groups_filename = os.environ['log_groups_filename']
    print(f'getting ... {log_groups_filename}')
    with open (log_groups_filename) as reader:
        log_group_policy = json.load(reader)


@then(u'I should see that the retention in days is set to {expected_retention_in_days}')
def step_impl(context, expected_retention_in_days):
    global log_group_policy, log_group_policy
    for log_group in log_group_policy['logGroups']:
        print(log_group['logGroupName'])
        if expected_log_group_name == log_group['logGroupName']:
            assert_that(int(log_group['retentionInDays']), equal_to(int(expected_retention_in_days)))
            return
    assert(False)