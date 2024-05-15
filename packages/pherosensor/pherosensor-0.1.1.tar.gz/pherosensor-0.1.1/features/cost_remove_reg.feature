Feature: remove regularization term to the cost function

Scenario: Test the method to remove regularization term to the cost function
    Given a mesh
    Given observations
    Given a control
    Given a cost function 
    When remove a regularization term
    When remove a regularization term not considered
    Then the attribute regularization_types is correctly updated
    Then the attribute alpha is correctly updated
    Then the attribute j_reg is correctly updated
    Then removing a regularization term not implemented raises exception
