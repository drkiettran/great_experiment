Feature: Queue Creation feature

Background: login background
    Given I am an ActiveMQ web console "http://localhost:8161"
    And I login using user "admin" and password "admin"

@wip
Scenario: Create a queue
    Given I at the Queue management page
    When I create a queue "my_queue"
    Then I should see "my_queue" in the active queue list
