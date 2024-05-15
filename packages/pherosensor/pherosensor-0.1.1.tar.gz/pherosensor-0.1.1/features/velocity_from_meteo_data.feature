Feature: velocity field from meteorological wind data

Scenario: interpolate the wind velocity data on the mesh
    Given a path to the data folder
    Given a name of the data file
    Given a rectangular 2D mesh
    When read the wind velocity data
    Then the time vector has the expected value
    And the matrix of the interpolated velocity field at the vertical interfaces has the expected value
    And the matrix of the interpolated velocity field at the horizontal interfaces has the expected value
