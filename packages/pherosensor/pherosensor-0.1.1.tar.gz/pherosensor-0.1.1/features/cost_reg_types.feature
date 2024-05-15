Feature: regularization types

Scenario: test the list of types of regularization
    Given a mesh
    Given observations
    Given a control
    When generate the Cost object with no regularization
    When generate the Cost object with one regularization
    When generate the Cost object with multiple regularizations
    Then the attribute regularization_types is a list
    And the attribute regularization_types has the expected value
    And input with wrong type raises exception
    And non string regularization type raises exception
    And not implemented regularization types raises exception
