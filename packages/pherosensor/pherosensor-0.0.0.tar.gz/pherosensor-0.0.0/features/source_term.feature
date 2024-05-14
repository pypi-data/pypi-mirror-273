Feature: the source term object

Scenario: Generate the source term as a Source object
    Given a time vector
    Given a source term
    Given an invalid source term
    Given a rectangular 2D mesh
    When initialize the Source object
    When initialize the steady Source object
    Then the source term has the expected value
    And the source term is correctly updated at a given time
    And the update at a given time does not change the values
    And the initialization fails if the number of dimension of the source term is not correct
    And the initialization fails if the source term shape does not match the shape of the mesh
    And the initialization fails if the source term shape does not match the shape of the time array
    And the update fails if the time is not between the lowest and largest times contained in the time vector
