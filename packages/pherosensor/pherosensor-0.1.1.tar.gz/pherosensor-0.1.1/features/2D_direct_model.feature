Feature: the DiffusionConvectionReaction2DEquation object

Scenario: Generate the DiffusionConvectionReaction2DEquation object for the resolution of the PDE
    Given a rectangular 2D mesh
    Given a velocity field
    Given a diffusion tensor
    Given a deposition coefficient
    Given a source term
    Given observations
    When initialize the DiffusionConvectionReaction2DEquation object
    When the output are saved
    Then the reaction term of the PDE is a linear operator
    And the convection term of the PDE is a linear operator
    And the diffusion term of the PDE is a linear operator
    And check the output of the solver has the expected shape
    And the output directory exists
    And the outputs are saved
    And the outputs have the expected shape
    And the saved outputs have the expected values
    And the solver at the observations times stores properly the estimation
    And the initialization fails if the given time discretization is not implemented
