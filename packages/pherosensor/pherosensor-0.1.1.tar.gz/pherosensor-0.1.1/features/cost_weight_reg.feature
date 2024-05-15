Feature: weight coefficients of the regularization terms

Scenario: test the dictionnary containing the weight coefficients of the regularization terms
    Given a mesh
    Given observations
    Given a control
    When generate the Cost object with no regularization
    When generate the Cost object with one regularization
    When generate the Cost object with multiple regularizations
    Then the attribute alpha is a dict
    And the attribute alpha has the expected value
    And input with wrong type raises exception
    And non float weight coefficient raises exception
    And different number of element in list of reg types and dict of weight coeff raises exception
    And difference between list of reg types and keys of dict of weight coeff raises exception
