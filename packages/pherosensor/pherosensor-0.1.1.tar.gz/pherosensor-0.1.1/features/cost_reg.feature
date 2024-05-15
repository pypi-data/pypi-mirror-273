Feature: reg cost

Scenario: Compute the regularization terms of the cost function and its gradients
    Given a mesh
    Given observations
    Given a control
    When generate the Cost object with no regularization
    When generate the Cost object with one regularization
    When generate the Cost object with multiple regularizations
    When compute the cost 
    Then the attribute j_reg is a dict
    And the cost has the expected value
    And the gradients have the expected values and shape
    And the proximal operator have the expected values and shape
    And computing the proximal operator for differentiable regularization term raises exception
