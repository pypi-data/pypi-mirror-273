Feature: 2D rectangular mesh object

Scenario: Generate a 2D rectangular mesh object
    Given length of the domain along the x axis
    Given length of the domain along the y axis
    Given a horizontal space step
    Given a vertical space step
    Given a final time
    Given coordinates of the origine
    When initialize the mesh
    When initialize the translated mesh
    When initialize the velocity field
    Then the vector of the x coordinates of the center of the cells has the expected size
    And the vector of the y coordinates of the center of the cells has the expected size
    And the vector of the x coordinates of the center of the cells has the expected value
    And the vector of the y coordinates of the center of the cells has the expected value
    And the vector of the translated x coordinates of the center of the cells has the expected value
    And the vector of the translated y coordinates of the center of the cells has the expected value
    And the vector of the x coordinates of the vertical interfaces between the cells has the expected size
    And the vector of the y coordinates of the horizontal interfaces between the cells has the expected size
    And the vector of the x coordinates of the vertical interfaces between the cells has the expected value
    And the vector of the y coordinates of the horizontal interfaces between the cells has the expected value
    And the measure of the control volume has the expected value
    And the expected time step is computed by the CFL condition
