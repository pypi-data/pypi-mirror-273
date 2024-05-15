Feature: the linear operator of the reaction term of the convection-diffusion PDE

Scenario: Generate the reaction term of the convection-diffusion PDE as a linear operator
    Given a deposition coefficient
    Given an invalid deposition coefficient
    Given a rectangular 2D mesh
    When initialize the reaction linear operator
    Then the reaction term is a linear operator
    And the result of the matrice vector product of the linear operator has the expected shape
    And the result of the matrice vector product of the linear operator has the expected values
    And the reaction coefficient is correctly updated
    And the initialization fails if the deposition coefficient shape does not match the shape of the mesh
