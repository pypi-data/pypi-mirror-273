from pathlib import Path

import numpy as np
from pytest_bdd import given
from pytest_bdd import scenario
from pytest_bdd import then
from pytest_bdd import when

from pheromone_dispersion.geom import MeshRect2D
from pheromone_dispersion.velocity import Velocity

"""
The mesh given by the data is the following:
 _ _
|_|_|
|_|_|
|_|_|
"""


@scenario("geometry.feature", "Generate a 2D rectangular mesh object")
def test_generate_mesh():
    """Generate the mesh."""


@given("length of the domain along the x axis", target_fixture="Lx")
def length_of_the_domain_along_the_x_axis():
    "length of the domain along the x-axis"
    return np.load(Path("tests/test_data") / "Lx.npy")


@given("length of the domain along the y axis", target_fixture="Ly")
def length_of_the_domain_along_the_y_axis():
    "length of the domain along the y-axis"
    return np.load(Path("tests/test_data") / "Ly.npy")


@given("a horizontal space step", target_fixture="dx")
def a_horizontal_space_step():
    "a horizontal space step"
    return np.load(Path("tests/test_data") / "dx.npy")


@given("a vertical space step", target_fixture="dy")
def a_vertical_space_step():
    "a vertical space step"
    return np.load(Path("tests/test_data") / "dy.npy")


@given("a final time", target_fixture="T_final")
def a_final_time():
    "a final time"
    return np.load(Path("tests/test_data") / "Tfinal.npy")


@given("coordinates of the origine", target_fixture="X_0")
def coordinates_of_the_origine():
    "coordinates of the origine"
    return (0, 3)


@when("initialize the mesh", target_fixture='msh')
def initialize_the_mesh(Lx, Ly, dx, dy, T_final):
    """initialize the mesh"""
    return MeshRect2D(Lx, Ly, dx, dy, T_final)


@when("initialize the translated mesh", target_fixture='msh_translated')
def initialize_the_translated_mesh(Lx, Ly, dx, dy, T_final, X_0):
    """initialize the translated mesh"""
    return MeshRect2D(Lx, Ly, dx, dy, T_final, X_0=X_0)


@when("initialize the velocity field", target_fixture="U")
def initialize_the_velocity_field(msh):
    "initialize the velocity field"
    t = np.load(Path("tests/test_data") / "t.npy")
    U_vi = np.load(Path("tests/test_data") / "U_vi.npy")
    U_hi = np.load(Path("tests/test_data") / "U_hi.npy")
    return Velocity(msh, U_vi, U_hi, t=t)


@then("the vector of the x coordinates of the center of the cells has the expected size")
def the_vector_of_the_x_coordinates_of_the_center_of_the_cells_has_the_expected_size(Lx, dx, msh, U):
    """the vector of the x coordinates of the center of the cells has the expected size"""
    assert msh.x.size == Lx // dx and msh.x.size == U.at_horizontal_interface.shape[1]


@then("the vector of the y coordinates of the center of the cells has the expected size")
def the_vector_of_the_y_coordinates_of_the_center_of_the_cells_has_the_expected_size(Ly, dy, msh, U):
    """the vector of the y coordinates of the center of the cells has the expected size"""
    assert msh.y.size == Ly // dy and msh.y.size == U.at_vertical_interface.shape[0]


@then("the vector of the x coordinates of the center of the cells has the expected value")
def the_vector_of_the_x_coordinates_of_the_center_of_the_cells_has_the_expected_value(msh):
    """the vector of the x coordinates of the center of the cells has the expected value"""
    assert (msh.x == [0.5, 1.5]).all()


@then("the vector of the y coordinates of the center of the cells has the expected value")
def the_vector_of_the_y_coordinates_of_the_center_of_the_cells_has_the_expected_value(msh):
    """the vector of the y coordinates of the center of the cells has the expected value"""
    assert (msh.y == [0.5, 1.5, 2.5]).all()


@then("the vector of the translated x coordinates of the center of the cells has the expected value")
def the_vector_of_the_translated_x_coordinates_of_the_center_of_the_cells_has_the_expected_value(msh_translated):
    """the vector of the translated x coordinates of the center of the cells has the expected value"""
    assert (msh_translated.x == [0.5, 1.5]).all()


@then("the vector of the translated y coordinates of the center of the cells has the expected value")
def the_vector_of_the_translated_y_coordinates_of_the_center_of_the_cells_has_the_expected_value(msh_translated):
    """the vector of the translated y coordinates of the center of the cells has the expected value"""
    print(msh_translated.y - [3.5, 4.5, 5.5])
    assert (msh_translated.y == [3.5, 4.5, 5.5]).all()


@then("the vector of the x coordinates of the vertical interfaces between the cells has the expected size")
def the_vector_of_the_x_coordinates_of_the_vertical_interfaces_between_the_cells_has_the_expected_size(Lx, dx, msh, U):
    """the vector of the x coordinates of the vertical interfaces between the cells has the expected size"""
    assert msh.x_vertical_interface.size == (Lx // dx + 1) and msh.x_vertical_interface.size == U.at_vertical_interface.shape[1]


@then("the vector of the y coordinates of the horizontal interfaces between the cells has the expected size")
def the_vector_of_the_y_coordinates_of_the_horizontal_interfaces_between_the_cells_has_the_expected_size(Ly, dy, msh, U):
    """the vector of the y coordinates of the horizontal interfaces between the cells has the expected size"""
    assert msh.y_horizontal_interface.size == (Ly // dy + 1) and msh.y_horizontal_interface.size == U.at_horizontal_interface.shape[0]


@then("the vector of the x coordinates of the vertical interfaces between the cells has the expected value")
def the_vector_of_the_x_coordinates_of_the_vertical_interfaces_between_the_cells_has_the_expected_value(msh):
    """the vector of the x coordinates of the vertical interfaces between the cells has the expected value"""
    assert (msh.x_vertical_interface == [0.0, 1.0, 2.0]).all()


@then("the vector of the y coordinates of the horizontal interfaces between the cells has the expected value")
def the_vector_of_the_y_coordinates_of_the_horizontal_interfaces_between_the_cells_has_the_expected_value(msh):
    """the vector of the y coordinates of the horizontal interfaces between the cells has the expected value"""
    assert (msh.y_horizontal_interface == [0.0, 1.0, 2.0, 3.0]).all()


@then("the measure of the control volume has the expected value")
def the_measure_of_the_control_volume_has_the_expected_value(msh):
    """the measure of the control volume has the expected value"""
    assert msh.mass_cell == 1


@then("the expected time step is computed by the CFL condition")
def the_expected_time_step_is_computed_by_the_CFL_condition(msh, U):
    """the expected time step is computed by the CFL condition"""
    msh.calc_dt_explicit_solver(U)
    assert msh.dt == 0.1
    # assert (msh.t_array == [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]).all()
    t = np.load(Path("tests/test_data") / "t.npy")
    V_vi = 3.0 * np.load(Path("tests/test_data") / "U_vi.npy")
    V_hi = 3.0 * np.load(Path("tests/test_data") / "U_hi.npy")
    msh.calc_dt_explicit_solver(Velocity(msh, V_vi, V_hi, t=t))
    assert msh.dt == 1.0 / (1.2 * 2 * 6)
    assert msh.T_final == 15.0 / (1.2 * 2 * 6)
