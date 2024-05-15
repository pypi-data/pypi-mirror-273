Feature:  modify the weight coefficient of a regularization term of the cost function

Scenario: Test the method to modify the weight of a regularization term
    Given a mesh
    Given observations
    Given a control
    Given a cost function 
    When modify a weight coefficient
    When set a weight coefficient to 0
    Then the attribute alpha is correctly updated
    Then modifying a regularization term not implemented raises exception
    Then modifying a regularization term not considered raises exception
