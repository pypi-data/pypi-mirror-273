Feature: Apply the control

Scenario: Apply the control to the direct model
    Given a mesh
    Given a control
    Given a direct model
    When apply the control to the direct model
    Then check the source term of the direct model has the expected value
