# -- FILE: features/environment.py
from behave import fixture, use_fixture
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

WEB_DRIVER_HOME = 'c:/dev/bin/chromedriver.exe'

def open_chrome_web_driver(web_driver_home, wait_time):
    web_driver = webdriver.Chrome(executable_path=web_driver_home)
    web_driver.implicitly_wait(wait_time)
    
    return web_driver

# Need Gecko Driver.
def open_firefox_web_driver(wait_time):
    print('Open Firefox webdriver')
    web_drive = webdriver.Firefox()
    
    web_driver.implicitly_wait(wait_time);
    return web_driver


@fixture
def selenium_browser_chrome(context):
    print('open driver')
    context.driver = open_chrome_web_driver(WEB_DRIVER_HOME, 5)
    #context.driver = open_firefox_web_driver(5)
    yield context.driver
    # -- CLEANUP-FIXTURE PART:
    print('quiting driver ...')
    context.driver.quit()

def before_all(context):
    print('before_all ...')
    use_fixture(selenium_browser_chrome, context)
    # -- HINT: CLEANUP-FIXTURE is performed after after_all() hook is called.

def after_all(context):
    print('after all ...')
