Feature: call of the optimization algorithm in minimize method

Scenario: Test the call to the different optimization algorithm in the minimize method
    Given a mesh
    Given environmental parameters
    Given a direct model
    Given observations
    Given an adjoint model
    Given a control
    When intialize a cost with a differentiable regularization term
    When intialize a cost with a non differentiable regularization term
    Then minimizing a non differentiable function with the gradient descent algorithm raises exception
    Then minimizing a non differentiable function with the L BFGS B algorithm raises exception
    Then minimizing a differentiable function with the proximal gradient algorithm raises exception
    And minimizing with a non implemented algorithm raises exception
