Feature: Velocity object with non-zero divergence

Scenario: Generate the non-zero deivergence velocity field as a velocity object
    Given a rectangular 2D mesh
    Given a time vector
    Given a velocity field at the vertical interfaces
    Given a velocity field at the horizontal interfaces
    When initialize the velocity object
    Then the matrix of the divergence of the velocity field has the expected shape
    And the matrix of the divergence of the velocity field has the expected values
    And the divergence of the velocity field is correctly updated at a given time
