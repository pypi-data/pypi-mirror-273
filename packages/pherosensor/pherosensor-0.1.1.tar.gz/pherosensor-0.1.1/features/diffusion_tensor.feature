Feature: Diffusion tensor

Scenario: Generate the diffusion tensor
    Given a rectangular 2D mesh
    Given a velocity field
    Given a steady velocity field
    Given a diffusion tensor in the wind direction
    Given a diffusion tensor in the crosswind direction
    When initialize the anisotrope diffusion tensor
    When initialize the steady anisotrope diffusion tensor
    Then the diffusion tensor at the vertical interfaces has the expected shape
    And the expected diffusion tensor at the vertical interfaces is computed
    And the diffusion tensor at the horizontal interfaces has the expected shape
    And the expected diffusion tensor at the horizontal interfaces is computed
    And the expected diffusion tensor at a given time is computed
    And the update fails if the time is not between the lowest and largest times contained in the time vector
    And the update at a given time of the steady diffusion tensor does not change the values
