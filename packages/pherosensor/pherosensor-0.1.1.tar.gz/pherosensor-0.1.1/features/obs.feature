Feature: Obs object

Scenario: Generate the obs object
    Given a rectangular 2D mesh
    Given the observations time
    Given the observations location
    Given the observations
    When generate the Obs object
    Then the vector of the position of the sensors has the expected shape and value
    Then the number of sensors has the expected value
    Then the vector of the index of the time of estimation has the expected shape and value
    Then the dictionnary containing the indexes of the observations given an estimation time has the expected values
    Then the initialization fails if the observations array has more than one dimension
    Then the initialization fails if the observations time array does not have the expected size
    Then the initialization fails if the observations location array does not have the expected size
    Then the initialization fails if the time array is not initialized
    Then the initialization fails if one of the observations is out of the spatial domain
    Then the initialization fails if one of the observations is out of the temporal domain
