Feature: outputs of the minimize method

Scenario: Test the outputs of the minimize method
    Given a mesh
    Given environmental parameters
    Given a direct model
    Given observations
    Given an adjoint model
    Given a control
    Given a maximum number of optimization iteration
    When intialize a cost
    When the cost function is minimized and the outputs saved
    Then the outputs have the expected type
    And the outputs have the expected size
    And the value of the control has been updated 
    And the output directory and files exist
    And the saved output have the expected values
