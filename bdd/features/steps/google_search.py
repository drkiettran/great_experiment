# file:features/steps/google_search.py
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

SEARCH_TEXT_BOX_XPATH = "//textarea[@name='q']"
GOOGLE_SEARCH_BUTTON_XPATH = "//input[@value='Google Search']"
RESULT_H3_XPATH = "//div[@id='rso']//h3"
DEMO_WAIT_TIME_IN_SECS = 3

def demo():
    time.sleep(DEMO_WAIT_TIME_IN_SECS)


def I_visit_the_website(context, website_url):
    print(f'\t** I opens the website @ "{website_url}"')
    context.driver.get(website_url)
    demo()

def I_enter_search_text(context, search_text):
    print(f'\t** I enter searching text "{search_text}"')
    wes = context.driver.find_elements(By.XPATH, SEARCH_TEXT_BOX_XPATH)
    if not wes:
        print('unable to locate data entry field ...')
        return
    
    wes[0].send_keys(search_text)
    demo()
    
def I_press_google_search_button(context, button_text):
    print(f'\t** I press the Google Search button')
    wes = context.driver.find_elements(By.XPATH, GOOGLE_SEARCH_BUTTON_XPATH)
    if not wes:
        print('unable to locate the search button {button_text}')
        return

    wes[0].click()
    demo()

def I_get_a_list_of_result_headings(context):
    print(f'\t** I am making a list of headings from the result')
    wes = context.driver.find_elements(By.XPATH, RESULT_H3_XPATH)
    if not wes:
        print('unable to locate the headings from the result')
        return
    heading_list = []
    for we in wes:
        heading_list.append(we.text)
    demo()
    return heading_list


@given(u'I am at a designated google website "{website_url}"')
def step_impl(context, website_url):
    I_visit_the_website(context, website_url)


@when(u'I search for "{search_text}"')
def step_impl(context, search_text):
    I_enter_search_text(context, search_text)
    I_press_google_search_button(context, 'Google Search')


@then(u'I should see a list of "{count}" or more search results')
def step_impl(context, count):
    global heading_list
    heading_list = I_get_a_list_of_result_headings(context)
    print(f'\t** I verify that I have more than {count} headings')
    assert_that(len(heading_list), greater_than(int(count)))

@then(u'the headline should be "{expected_search_result}"')
def step_impl(context, expected_search_result):
    search_result = heading_list[0]
    print(f'\t** I verify that the first heading is equal to "{expected_search_result}"')
    assert_that(search_result, equal_to(expected_search_result))