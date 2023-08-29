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
@given(u'I login using user "{user}" and password "{password}"')
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

@when(u'I create a queue "{queue_name}"')
def step_impl(context, queue_name):
    context.queue_name = queue_name


    # enter queue name
    elems = context.driver.find_elements(By.XPATH, "//input[@name='JMSDestination']")
    if not elems:
        assert(False)
        return    
    elems[0].send_keys(queue_name)
    
    # click on Create button
    elems = context.driver.find_elements(By.XPATH, "//input[@type='submit' and @value='Create']")
    if not elems:
        assert(False)
        return
    elems[0].click()

    demo()    
    

@then(u'I should see "{queue_name}" in the active queue list')
def step_impl(context, queue_name):
    elems = context.driver.find_elements(By.XPATH, f"//td/a[contains(text(),'{queue_name}')]")
    if not elems:
        assert(False)
        return
    text = elems[0].text
    assert_that(text, equal_to(queue_name))

    # search and remove the queue we just created as a part of cleanup activities
    elems = context.driver.find_elements(By.XPATH, 
                                         "//td/a[contains(text(),'my_queue')]/../../td[7]/a[contains(text(),'Delete')]")
    if not elems:
        assert(False)
        return
    elems[0].click()

@given(u'I at the Queue management page')
def step_impl(context):
    # go to manage activeMQ broker
    elems = context.driver.find_elements(By.XPATH, "//a[@title='Manage ActiveMQ broker']")
    if not elems:
        assert(False)
        return
    elems[0].click()

    # go to Queues page
    elems = context.driver.find_elements(By.XPATH, "//a[@title='Queues']")
    if not elems:
        assert(False)
        return
    elems[0].click()