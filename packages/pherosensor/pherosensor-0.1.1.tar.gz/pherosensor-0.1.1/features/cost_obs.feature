Feature: obs cost

Scenario: Compute the observation term of the cost function and its gradient
    Given a mesh
    Given observations
    Given a control
    When generate the Cost object
    When compute the cost 
    Then the cost is a float
    And the cost has the expected value
    And the gradient of the objectif function with respect to the observed variable has the expected shape
    And the gradient of the objectif function with respect to the observed variable has the expected values
    And computing the gradient with respect to the observed variable without estimating the observed variable raises exception
