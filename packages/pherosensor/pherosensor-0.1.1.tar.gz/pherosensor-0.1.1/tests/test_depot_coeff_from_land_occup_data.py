from pathlib import Path

import numpy as np
import pytest
from pytest_bdd import given
from pytest_bdd import scenario
from pytest_bdd import then
from pytest_bdd import when

from pheromone_dispersion.deposition_coeff import deposition_coeff_from_land_occupation_data
from pheromone_dispersion.geom import MeshRect2D


@scenario("depot_coeff_from_land_occup_data.feature", "Generate deposition coefficient from land occupation data")
def test_generate_deposition_coefficient_from_land_occupation_data():
    """Generate deposition coefficient from land occupation data."""


@given("a rectangular 2D mesh", target_fixture="msh")
def a_rectangular_2D_mesh():
    "a rectangular 2D mesh"
    Lx = np.load(Path("tests/test_data") / "Lx.npy")
    Ly = np.load(Path("tests/test_data") / "Ly.npy")
    dx = np.load(Path("tests/test_data") / "dx.npy")
    dy = np.load(Path("tests/test_data") / "dy.npy")
    Tfinal = np.load(Path("tests/test_data") / "Tfinal.npy")
    return MeshRect2D(Lx, Ly, dx, dy, Tfinal)


@given("the deposition coefficient wrt the land occupation", target_fixture="land_occupation_to_deposition_coeff")
def the_deposition_coefficient_wrt_the_land_occupation():
    "the deposition coefficient wrt the land occupation"
    return {'box 1': 3.14, 'box 2': 42, 'box 3': 2.71}


@given("the path to the folder containing the data", target_fixture="path_data")
def the_path_to_the_folder_containing_the_data():
    "the path to the folder containing the data"
    return "tests/test_data"


@given("the name of the file containing the data", target_fixture="file_name_data")
def the_name_of_the_file_containing_the_data():
    "the name of the file containing the data"
    return "land_occupation.shp"


@when("generate the deposition coefficient", target_fixture='depot_coeff')
def generate_the_deposition_coefficient(path_data, file_name_data, land_occupation_to_deposition_coeff, msh):
    """generate the deposition coefficient"""
    return deposition_coeff_from_land_occupation_data(path_data, file_name_data, land_occupation_to_deposition_coeff, msh)


@then("the matrix of the deposition coefficient has the expected shape")
def the_matrix_of_the_deposition_coefficient_has_the_expected_shape(msh, depot_coeff):
    """the matrix of the deposition coefficient has the expected shape"""
    assert depot_coeff.shape == (msh.y.size, msh.x.size)


@then("the matrix of the deposition coefficient has the expected values")
def the_matrix_of_the_deposition_coefficient_has_the_expected_values(depot_coeff):
    """the matrix of the deposition coefficient has the expected values"""
    truth = [[3.14, 42], [2.71, 42], [2.71, 0]]
    assert (depot_coeff == truth).all()


@then("the generation fails if one of the classification is not in the deposition coefficient wrt the land occupation data")
def the_generation_fails_if_one_of_the_classification_is_not_in_the_deposition_coefficient_wrt_the_land_occupation_data(
    path_data, file_name_data, msh
):
    "the generation fails if one of the classification is not in the deposition coefficient wrt the land occupation data"
    land_occupation_to_deposition_coeff_fail = {'box 1': 3.14, 'box 2': 42}
    with pytest.raises(ValueError) as e:
        deposition_coeff_from_land_occupation_data(path_data, file_name_data, land_occupation_to_deposition_coeff_fail, msh)
    assert e.type == ValueError
