Feature: gradient descent method

Scenario: Test the gradient descent method
    Given a function to minimize and its gradient
    Given an initial point
    Given a step size
    Given a too big step size
    Given a number of iteration
    Given a callback function
    When the gradient descent algorithm is performed
    Then the termination criteria is reached
    Then the outputs of the gradient descent algorithm have the expected values
    Then the callback function has been executed at each iteration
    Then the algorithm fails if function does not decreases
