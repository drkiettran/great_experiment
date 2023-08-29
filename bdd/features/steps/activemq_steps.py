# file:features/steps/activemq_steps.py
# ----------------------------------------------------------------------------
# STEPS:
# ----------------------------------------------------------------------------
from behave   import given, when, then
from hamcrest import assert_that, equal_to, greater_than
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import logging
import time

DEMO_WAIT_TIME_IN_SECS = 2

def demo():
    time.sleep(DEMO_WAIT_TIME_IN_SECS)

@given(u'I am an ActiveMQ web console "{website_url}"')
def step_impl(context, website_url):
    context.activemq_website_url = website_url
    print(f'\t** I open ActiveMQ web console @ "{context.activemq_website_url}"')
    # context.driver.get(website_url)
    # demo()


@when(u'I login using user "{user}" and password "{password}"')
def step_impl(context, user, password):
    url = context.activemq_website_url.replace("://", f'://{user}:{password}@')
    print(f'\t** I login to {url}')
    context.driver.get(url)
    demo()

@then(u'I should be on the main website')
def step_impl(context):
    print(f'\t** I verify welcome page ...')
    elems = context.driver.find_elements(By.XPATH, '//h2')

    if elems:
        text = elems[0].text
    else:
        text = '**notfound**'

    assert_that(text, equal_to("Welcome to the Apache ActiveMQ!"))
    demo()
    