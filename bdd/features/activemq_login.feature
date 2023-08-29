Feature: login to Active MQ

Scenario: Login to ActiveMQ web console

Given I am an ActiveMQ web console "http://localhost:8161"
When I login using user "admin" and password "admin"
Then I should be on the main website

