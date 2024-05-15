from pathlib import Path

import numpy as np
from pytest_bdd import given
from pytest_bdd import scenario
from pytest_bdd import then
from pytest_bdd import when

from pheromone_dispersion.geom import MeshRect2D
from pheromone_dispersion.velocity import velocity_field_from_meteo_data


@scenario("velocity_from_meteo_data.feature", "interpolate the wind velocity data on the mesh")
def test_interpolate_the_wind_velocity_data_on_the_mesh():
    """Interpolate the wind velocity data on the mesh."""


@given("a path to the data folder", target_fixture="path")
def a_path_to_the_data_folder():
    "a path to the data folder"
    return "tests/test_data"


@given("a name of the data file", target_fixture="file_name")
def a_name_of_the_data_file():
    "a name of the data file"
    return 'df_test.csv'


@given("a rectangular 2D mesh", target_fixture="msh")
def a_rectangular_2D_mesh():
    "a rectangular 2D mesh"
    Lx = np.load(Path("tests/test_data") / "Lx.npy")
    Ly = np.load(Path("tests/test_data") / "Ly.npy")
    dx = np.load(Path("tests/test_data") / "dx.npy")
    dy = np.load(Path("tests/test_data") / "dy.npy")
    Tfinal = np.load(Path("tests/test_data") / "Tfinal.npy")
    return MeshRect2D(Lx, Ly, dx, dy, Tfinal - 1e-15)


@when("read the wind velocity data", target_fixture='U')
def read_the_wind_velocity_data(path, file_name, msh):
    "read the wind velocity data"
    return velocity_field_from_meteo_data(path, file_name, msh)


@then("the time vector has the expected value")
def the_time_vector_has_the_expected_value(U):
    "the time vector has the expected value"
    assert (U.t == [0.0, 1.0]).all()


@then("the matrix of the interpolated velocity field at the vertical interfaces has the expected value")
def the_matrix_of_the_interpolated_velocity_field_at_the_vertical_interfaces_has_the_expected_value(U):
    "the matrix of the interpolated velocity field at the vertical interfaces has the expected value"
    truth = [[[1, 0.25], [2, -0.75], [3, -1.75]], [[3, 0.75], [4, -0.25], [5, -1.25]], [[5, 1.25], [6, 0.25], [7, -0.75]]]
    assert np.max(np.abs(U.at_vertical_interface - truth)) < 1e-15  # (U.at_vertical_interface == truth).all()


@then("the matrix of the interpolated velocity field at the horizontal interfaces has the expected value")
def the_matrix_of_the_interpolated_velocity_field_at_the_horizontal_interfaces_has_the_expected_value(U):
    "the matrix of the interpolated velocity field at the horizontal interfaces has the expected value"
    truth = [[[0.5, -0.5], [1.5, -1.5]], [[2.5, 0.0], [3.5, -1.0]], [[4.5, 0.5], [5.5, -0.5]], [[6.5, 1.0], [7.5, 0.0]]]
    # print(np.max(np.abs(U.at_horizontal_interface - truth)))
    assert np.max(np.abs(U.at_horizontal_interface - truth)) < 1e-15  # (U.at_horizontal_interface == truth).all()
