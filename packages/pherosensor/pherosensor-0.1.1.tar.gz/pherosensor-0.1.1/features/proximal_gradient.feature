Feature: proximal gradient method

Scenario: Test the proximal gradient method
    Given the differentiable part of a function to minimize and its gradient
    Given the proximal operator of the other part of the function to minimize
    Given an initial point
    Given a step size
    Given a number of iteration
    Given a callback function
    When the proximal gradient algorithm is performed
    Then the termination criteria is reached
    Then the outputs of the proximal gradient algorithm have the expected values
    Then the callback function has been executed at each iteration
    Then the method fails if the type of algorithm is not implemented
