Feature: the deposition_coeff_from_land_occupation_data method

Scenario: Generate deposition coefficient from land occupation data
    Given a rectangular 2D mesh
    Given the deposition coefficient wrt the land occupation
    Given the path to the folder containing the data
    Given the name of the file containing the data
    When generate the deposition coefficient
    Then the matrix of the deposition coefficient has the expected shape
    Then the matrix of the deposition coefficient has the expected values
    Then the generation fails if one of the classification is not in the deposition coefficient wrt the land occupation data
