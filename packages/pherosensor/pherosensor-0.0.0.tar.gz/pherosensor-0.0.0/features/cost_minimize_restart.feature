Feature: restarting minimize method

Scenario: Test the restart process of the minimize method
    Given a mesh
    Given environmental parameters
    Given a direct model
    Given observations
    Given an adjoint model
    Given a control
    Given a maximum number of optimization iteration
    Given a cost function
    When the cost is minimized at one go
    When the cost is minimized with a restart
    Then the outputs of the optimization with restart have the expected values
    And restarting optimization with an invalid directory raises exception
    And restarting optimization with missing files in the directory raises exception
