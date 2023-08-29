Feature: login to Active MQ

Scenario: Login to ActiveMQ web console

Given I am an ActiveMQ web console "http://localhost:8161"
When I login using user "admin" and password "admin"
Then I should be on the main website

@wip
Scenario: Create a queue
Given I am an ActiveMQ web console "http://localhost:8161"
And I login using user "admin" and password "admin"
When I create a queue "my_queue"
Then I should see "my_queue" in the active queue list
