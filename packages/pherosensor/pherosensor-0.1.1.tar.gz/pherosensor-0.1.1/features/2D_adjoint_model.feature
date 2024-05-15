Feature: the AdjointDiffusionConvectionReaction2DEquation object

Scenario: Generate the AdjointDiffusionConvectionReaction2DEquation object for the resolution of the PDE
    Given a rectangular 2D mesh
    Given a velocity field
    Given a diffusion tensor
    Given a deposition coefficient
    Given observations
    Given cost
    When initialize the AdjointDiffusionConvectionReaction2DEquation object with semi implicit discretization
    When initialize the AdjointDiffusionConvectionReaction2DEquation object with implicit discretization
    Then the reaction term of the PDE is a linear operator
    And the diffusion term of the PDE is a linear operator
    And the convection term of the semi implicit PDE is a linear operator
    And the div parts of the convection term of the semi implicit PDE have the expected values
    And the convection term of the implicit PDE is a linear operator
    And the output of the solver has the expected shape
    And the initialization fails if the given time discretization is not implemented
