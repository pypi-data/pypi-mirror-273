Feature: Gaussian plumes

Scenario: Generate and compute the Gaussian plume
    Given a rectangular 2D mesh
    Given a source location
    Given an emission rate of the source
    Given a constant diffusion coefficient
    Given a constant wind velocity
    Given a settling velocity
    Given a deposition velocity
    When initialize the single source gaussian plume
    When initialize the multiple sources gaussian plume
    Then the change of variable has the expected shape
    And the change of variable has the expected value
    And the single source gaussian plume has the expected shape
    And the single source gaussian plume has the expected value
    And the multiple sources gaussian plume has the expected shape
    And the multiple sources gaussian plume has the expected value with one source
