from pathlib import Path

import numpy as np
import pytest
from pytest_bdd import given
from pytest_bdd import scenario
from pytest_bdd import then
from pytest_bdd import when

from pheromone_dispersion.geom import MeshRect2D
from pheromone_dispersion.velocity import Velocity


@scenario("steady_velocity_field.feature", "Generate the steady velocity field as a velocity object")
def test_generate_velocity_field_as_velocity_object():
    """Generate the velocity field as a velocity object."""


@given("a rectangular 2D mesh", target_fixture="msh")
def a_rectangular_2D_mesh():
    "a rectangular 2D mesh"
    Lx = np.load(Path("tests/test_data") / "Lx.npy")
    Ly = np.load(Path("tests/test_data") / "Ly.npy")
    dx = np.load(Path("tests/test_data") / "dx.npy")
    dy = np.load(Path("tests/test_data") / "dy.npy")
    Tfinal = np.load(Path("tests/test_data") / "Tfinal.npy")
    return MeshRect2D(Lx, Ly, dx, dy, Tfinal)


@given("a velocity field at the vertical interfaces", target_fixture='U_vi')
def a_velocity_field_at_the_vertical_interfaces():
    "a velocity field at the vertical interfaces"
    U_vi = np.load(Path("tests/test_data") / "U_vi.npy")
    return U_vi[0, :, :, :]


@given("a velocity field at the horizontal interfaces", target_fixture='U_hi')
def a_velocity_field_at_the_horizontal_interfaces():
    "a velocity field at the horizontal interfaces"
    U_hi = np.load(Path("tests/test_data") / "U_hi.npy")
    return U_hi[0, :, :, :]


@when("initialize the velocity object", target_fixture='U')
def initialize_the_velocity_object(msh, U_vi, U_hi):
    """initialize the velocity object"""
    return Velocity(msh, U_vi, U_hi)


@then("the time vector is None")
def the_time_vector_is_None(U):
    """the time vector is None"""
    assert U.t is None


@then("the matrix of the velocity field at the vertical interfaces has the expected shape")
def the_matrix_of_the_velocity_field_at_the_vertical_interfaces_has_the_expected_shape(U):
    """the matrix of the velocity field at the vertical interfaces has the expected shape"""
    assert U.at_vertical_interface.shape == (3, 3, 2)


@then("the matrix of the velocity field at the vertical interfaces has the expected values")
def the_matrix_of_the_velocity_field_at_the_vertical_interfaces_has_the_expected_values(U):
    """the matrix of the velocity field at the vertical interfaces has the expected values"""
    assert (U.at_vertical_interface == 1).all()


@then("the matrix of the velocity field at the horizontal interfaces has the expected shape")
def the_matrix_of_the_velocity_field_at_the_horizontal_interfaces_has_the_expected_shape(U):
    """the matrix of the velocity field at the horizontal interfaces has the expected shape"""
    assert U.at_horizontal_interface.shape == (4, 2, 2)


@then("the matrix of the velocity field at the horizontal interfaces has the expected values")
def the_matrix_of_the_velocity_field_at_the_horizontal_interfaces_has_the_expected_values(U):
    """the matrix of the velocity field at the horizontal interfaces has the expected values"""
    assert (U.at_horizontal_interface == 1).all()


@then("the matrix of the divergence of the velocity field has the expected shape")
def the_matrix_of_the_divergence_of_the_velocity_field_has_the_expected_shape(U):
    """the matrix of the divergence of the velocity field has the expected shape"""
    assert U.div.shape == (3, 2)


@then("the matrix of the divergence of the velocity field has the expected values")
def the_matrix_of_the_divergence_of_the_velocity_field_has_the_expected_values(U):
    """the matrix of the divergence of the velocity field has the expected values"""
    assert (U.div == 0).all()


@then("the matrices of boolean of the upwind cells has the expected shape")
def the_matrices_of_boolean_of_the_upwind_cells_has_the_expected_shape(msh, U):
    """the matrices of boolean of the upwind cells has the expected shape"""
    assert U.cell_above_upwind.shape == (msh.y_horizontal_interface.size, msh.x.size)
    assert U.cell_under_upwind.shape == (msh.y_horizontal_interface.size, msh.x.size)
    assert U.cell_left_upwind.shape == (msh.y.size, msh.x_vertical_interface.size)
    assert U.cell_right_upwind.shape == (msh.y.size, msh.x_vertical_interface.size)


@then("the matrices of boolean of the upwind cells has the expected values")
def the_matrices_of_boolean_of_the_upwind_cells_has_the_expected_values(U):
    """the matrices of boolean of the upwind cells has the expected values"""
    assert not (U.cell_above_upwind).all()
    assert U.cell_under_upwind.all()
    assert U.cell_left_upwind.all()
    assert not (U.cell_right_upwind).all()


@then("the maximum of the horizontal velocity has the expected value")
def the_maximum_of_the_horizontal_velocity_has_the_expected_value(U):
    """the maximum of the horizontal velocity has the expected value"""
    assert U.max_horizontal_U == 1


@then("the maximum of the vertical velocity has the expected value")
def the_maximum_of_the_vertical_velocity_has_the_expected_value(U):
    """the maximum of the vertical velocity has the expected value"""
    assert U.max_vertical_U == 1


@then("the initialization fails if the number of dimension of the velocity field is not correct")
def the_initialization_fails_if_the_number_of_dimension_of_the_velocity_field_is_not_correct(U_vi, U_hi, msh):
    """the initialization fails if the number of dimension of the velocity is not correct"""
    with pytest.raises(ValueError) as e:
        Velocity(msh, U_vi[:, :, 0], U_hi)
    assert e.type == ValueError
    with pytest.raises(ValueError) as e:
        Velocity(msh, U_vi, U_hi[:, :, 0])
    assert e.type == ValueError


@then("the initialization fails if the velocity fields shape do not match")
def the_initialization_fails_if_the_velocity_fields_shape_do_not_match(msh, U_vi, U_hi):
    """the initialization fails if the velocity fields shape do not match"""
    with pytest.raises(ValueError) as e:
        Velocity(msh, U_hi, U_vi)
    assert e.type == ValueError


@then("the update at a given time does not change the values")
def the_update_at_a_given_time_does_not_change_the_values(U):
    """the update at a given time does not change the values"""
    U_hi = np.copy(U.at_horizontal_interface)
    U_vi = np.copy(U.at_vertical_interface)
    cell_above_upwind = np.copy(U.cell_above_upwind)
    cell_under_upwind = np.copy(U.cell_under_upwind)
    cell_right_upwind = np.copy(U.cell_right_upwind)
    cell_left_upwind = np.copy(U.cell_left_upwind)
    U.at_current_time(1.5)
    assert (U_hi == U.at_horizontal_interface).all()
    assert (U_vi == U.at_vertical_interface).all()
    assert (cell_above_upwind == U.cell_above_upwind).all()
    assert (cell_under_upwind == U.cell_under_upwind).all()
    assert (cell_right_upwind == U.cell_right_upwind).all()
    assert (cell_left_upwind == U.cell_left_upwind).all()
