Feature: Velocity object

Scenario: Generate the velocity field as a Velocity object
    Given a rectangular 2D mesh
    Given a time vector
    Given a velocity field at the vertical interfaces
    Given a velocity field at the horizontal interfaces
    Given an invalid velocity field at the vertical interfaces
    Given an invalid velocity field at the horizontal interfaces
    When initialize the velocity object
    Then the matrix of the velocity field at the vertical interfaces has the expected shape
    And the matrix of the velocity field at the vertical interfaces has the expected values
    And the matrix of the velocity field at the horizontal interfaces has the expected shape
    And the matrix of the velocity field at the horizontal interfaces has the expected values
    And the matrices of boolean of the upwind cells has the expected shape
    And the matrices of boolean of the upwind cells has the expected values
    And the velocity field is correctly updated at a given time
    And the maximum of the horizontal velocity has the expected value
    And the maximum of the vertical velocity has the expected value
    And the initialization fails if the number of dimension of the velocity field is not correct
    And the initialization fails if the velocity fields shape do not match the shape of the mesh
    And the initialization fails if the velocity fields shape do not match at vertical and horizontal interfaces
    And the initialization fails if the velocity fields shape do not match with the shape of the time vector
    And the update fails if the time is not between the lowest and largest times contained in the time vector
