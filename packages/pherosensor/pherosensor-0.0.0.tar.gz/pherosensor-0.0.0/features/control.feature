Feature: the Control object

Scenario: Generate the Control object
    Given a rectangular 2D mesh
    Given a source term
    When initialize the Control object
    Then check the array of the background values has the expected shape
    And check the array of the current values has the expected shape
    And check the array of the background values has the expected values
    And check the array of the current values has the expected values
    And the initialization fails if the time array is not initialized
