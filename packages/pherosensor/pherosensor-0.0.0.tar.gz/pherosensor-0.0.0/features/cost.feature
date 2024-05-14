Feature: Cost object

Scenario: Generate the Cost object and compute the cost function
    Given a mesh
    Given observations
    Given a control
    When generate the Cost object
    When compute the cost 
    Then the cost is a float
    And the cost has the expected value
    And Computing the cost without estimating the observed variable raises exception
