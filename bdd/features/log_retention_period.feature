Feature: Log Retention Period check

Scenario: Verify log rention period is provisioned correctly
Given I have a log group "my-log-group-2" retention policy
When I retrieve the rention policy
Then I should see that the retention in days is set to 30