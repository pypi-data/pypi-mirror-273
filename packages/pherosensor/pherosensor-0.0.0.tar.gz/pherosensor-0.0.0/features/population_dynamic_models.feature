Feature: Population dynamic models

Scenario: Generate and compute the population dynamic models
    Given a mesh
    When generate the population dynamic model
    When generate the stationnary population dynamic model
    Then the estimation of the population dynamic models has the expected shape and values
    And the estimation of the adjoint of the population dynamic models has the expected shape and values
