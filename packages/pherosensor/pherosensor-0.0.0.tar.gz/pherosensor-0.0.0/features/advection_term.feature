Feature: the linear operator of the convection term

Scenario: Generate the convection term of the convection-diffusion PDE as a linear operator
    Given a rectangular 2D mesh
    Given a velocity field
    When initialize the convection linear operator
    Then the convection term is a linear operator
    And the result of the matrice vector product of the linear operator has the expected shape
    And the result of the matrice vector product of the linear operator has the expected values
    And the opposite sign velocity field is a Velocity object
    And the opposite sign velocity field has the expected value
    And the result of the matrice vector product of the flux part of the adjoint operator has the expected shape
    And the result of the matrice vector product of the flux part of the adjoint operator has the expected value
    And the linear operator is updated as expected at a given time
