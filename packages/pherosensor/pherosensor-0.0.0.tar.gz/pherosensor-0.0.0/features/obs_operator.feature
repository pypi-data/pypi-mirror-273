Feature: the observation operator

Scenario: test the observation operator
    Given a rectangular 2D mesh
    Given an Obs object
    Given an estimate of the state variable of the direct model
    When estimate the observed variable 
    Then the estimation of the observed variable has the expected size
    Then the estimation of the observed variable has the expected value
    Then the result of the adjoint of the derivative of the obs operator has the expected value
    Then the result of the adjoint of the derivative of the one sensor obs operator has the expected value
    Then the estimation of the observed variable fails if the estimation of the state variable is not initialized
    Then the initialization fails if the observation operator integration time window is out of the temporal domain
    Then the initialization fails if the observation operator time window overlapps for two data of a same sensor
