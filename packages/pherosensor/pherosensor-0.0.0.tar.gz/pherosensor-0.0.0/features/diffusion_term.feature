Feature: the linear operator of the diffusion term of the convection-diffusion PDE

Scenario: Generate the diffusion term of the convection-diffusion PDE as a linear operator
    Given a rectangular 2D mesh
    Given a diffusion tensor
    Given a steady diffusion tensor
    When initialize the diffusion linear operator
    When initialize the steady diffusion linear operator
    Then the diffusion term is a linear operator
    And the result of the matrice vector product of the linear operator has the expected shape
    And the result of the matrice vector product of the linear operator has the expected values
    And the linear operator is updated as expected at a given time
    And the update at a given time of the steady linear operator does not change the values
