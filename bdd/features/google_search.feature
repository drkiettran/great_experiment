Feature: Searching for text at a google search website
    As a Google user,
    I want to search for any text that may exist in the Internet
    So that I can do my research more effectively

    Scenario: Searching for random text    
        Given I am at a designated google website "https://google.com"
        When I search for "selenium webdriver"
        Then I should see a list of "1" or more search results
        And the headline should be "WebDriver"


