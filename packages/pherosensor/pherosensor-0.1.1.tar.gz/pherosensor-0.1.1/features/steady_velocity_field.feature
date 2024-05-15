Feature: Velocity object

Scenario: Generate the steady velocity field as a velocity object
    Given a rectangular 2D mesh
    Given a velocity field at the vertical interfaces
    Given a velocity field at the horizontal interfaces
    When initialize the velocity object
    Then the time vector is None
    Then the matrix of the velocity field at the vertical interfaces has the expected shape
    Then the matrix of the velocity field at the vertical interfaces has the expected values
    Then the matrix of the velocity field at the horizontal interfaces has the expected shape
    Then the matrix of the velocity field at the horizontal interfaces has the expected values
    And the matrix of the divergence of the velocity field has the expected shape
    And the matrix of the divergence of the velocity field has the expected values
    And the matrices of boolean of the upwind cells has the expected shape
    And the matrices of boolean of the upwind cells has the expected values
    And the maximum of the horizontal velocity has the expected value
    And the maximum of the vertical velocity has the expected value
    And the initialization fails if the number of dimension of the velocity field is not correct
    Then the initialization fails if the velocity fields shape do not match
    Then the update at a given time does not change the values
