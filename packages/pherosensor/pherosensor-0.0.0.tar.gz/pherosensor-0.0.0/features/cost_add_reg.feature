Feature: add regularization term to the cost function

Scenario: Test the method to add regularization term to the cost function
    Given a mesh
    Given observations
    Given a control
    Given a cost function 
    When add a regularization term
    When add a regularization term already considered
    When add a regularization term with weight equals to 0
    Then the attribute regularization_types is correctly updated
    Then the attribute alpha is correctly updated
    Then the attribute j_reg is correctly updated
    Then adding a regularization term not implemented raises exceptions
