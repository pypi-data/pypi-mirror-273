from pathlib import Path

import numpy as np
import pytest
from pytest_bdd import given
from pytest_bdd import scenario
from pytest_bdd import then
from pytest_bdd import when

from pheromone_dispersion.geom import MeshRect2D
from pheromone_dispersion.velocity import Velocity


@scenario("velocity_field.feature", "Generate the velocity field as a Velocity object")
def test_generate_velocity_field_as_Velocity_object():
    """Generate the velocity field as a Velocity object."""


@given("a rectangular 2D mesh", target_fixture="msh")
def a_rectangular_2D_mesh():
    "a rectangular 2D mesh"
    Lx = np.load(Path("tests/test_data") / "Lx.npy")
    Ly = np.load(Path("tests/test_data") / "Ly.npy")
    dx = np.load(Path("tests/test_data") / "dx.npy")
    dy = np.load(Path("tests/test_data") / "dy.npy")
    Tfinal = np.load(Path("tests/test_data") / "Tfinal.npy")
    return MeshRect2D(Lx, Ly, dx, dy, Tfinal)


@given("a time vector", target_fixture='t')
def a_time_vector():
    "a time vector"
    t = np.load(Path("tests/test_data") / "t.npy")
    return t


@given("a velocity field at the vertical interfaces", target_fixture='U_vi')
def a_velocity_field_at_the_vertical_interfaces():
    "a velocity field at the vertical interfaces"
    U_vi = np.load(Path("tests/test_data") / "U_vi.npy")
    return U_vi


@given("a velocity field at the horizontal interfaces", target_fixture='U_hi')
def a_velocity_field_at_the_horizontal_interfaces():
    "a velocity field at the horizontal interfaces"
    U_hi = np.load(Path("tests/test_data") / "U_hi.npy")
    return U_hi


@given("an invalid velocity field at the vertical interfaces", target_fixture='U_vi_invalid')
def an_invalid_velocity_field_at_the_vertical_interfaces():
    "an invalid velocity field at the vertical interfaces"
    U_vi_invalid = np.load(Path("tests/test_data") / "U_vi_invalid.npy")
    return U_vi_invalid


@given("an invalid velocity field at the horizontal interfaces", target_fixture='U_hi_invalid')
def an_invalid_velocity_field_at_the_horizontal_interfaces():
    "an invalid velocity field at the horizontal interfaces"
    U_hi_invalid = np.load(Path("tests/test_data") / "U_hi_invalid.npy")
    return U_hi_invalid


@when("initialize the velocity object", target_fixture='U')
def initialize_the_velocity_object(msh, t, U_vi, U_hi):
    """initialize the velocity object"""
    return Velocity(msh, U_vi, U_hi, t=t)


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


@then("the velocity field is correctly updated at a given time")
def the_velocity_field_is_correctly_updated_at_a_given_time(U):
    """the velocity field is correctly updated at a given time"""
    U.at_current_time(1 / 2)
    assert (U.at_horizontal_interface[:, :, 0] == 1.5).all() and (U.at_horizontal_interface[:, :, 1] == -0.5).all()
    assert (U.at_vertical_interface[:, :, 0] == 1.5).all() and (U.at_vertical_interface[:, :, 1] == -0.5).all()
    assert U.cell_above_upwind.all()
    assert not (U.cell_under_upwind).all()
    assert U.cell_left_upwind.all()
    assert not (U.cell_right_upwind).all()


@then("the maximum of the horizontal velocity has the expected value")
def the_maximum_of_the_horizontal_velocity_has_the_expected_value(U):
    """the maximum of the horizontal velocity has the expected value"""
    assert U.max_horizontal_U == 2


@then("the maximum of the vertical velocity has the expected value")
def the_maximum_of_the_vertical_velocity_has_the_expected_value(U):
    """the maximum of the vertical velocity has the expected value"""
    assert U.max_vertical_U == 2


@then("the initialization fails if the number of dimension of the velocity field is not correct")
def the_initialization_fails_if_the_number_of_dimension_of_the_velocity_field_is_not_correct(U_vi, U_hi, t, msh):
    """the initialization fails if the number of dimension of the velocity is not correct"""
    with pytest.raises(ValueError) as e:
        Velocity(msh, U_vi[:, :, :, 0], U_hi, t=t)
    assert e.type == ValueError
    with pytest.raises(ValueError) as e:
        Velocity(msh, U_vi, U_hi[:, :, :, 0], t=t)
    assert e.type == ValueError


@then("the initialization fails if the velocity fields shape do not match the shape of the mesh")
def the_initialization_fails_if_the_velocity_fields_shape_do_not_match_the_shape_of_the_mesh(msh, U_hi_invalid, U_vi_invalid):
    """the initialization fails if the velocity fields shape do not match the shape of the mesh"""
    with pytest.raises(ValueError) as e:
        Velocity(msh, U_vi_invalid, U_hi_invalid)
    assert e.type == ValueError


@then("the initialization fails if the velocity fields shape do not match at vertical and horizontal interfaces")
def the_initialization_fails_if_the_velocity_fields_shape_do_not_match_at_vertical_and_horizontal_interfaces(msh, t, U_vi, U_hi):
    """the initialization fails if the velocity fields shape do not match at vertical and horizontal interfaces"""
    with pytest.raises(ValueError) as e:
        Velocity(msh, U_hi, U_vi, t=t)
    assert e.type == ValueError


@then("the initialization fails if the velocity fields shape do not match with the shape of the time vector")
def the_initialization_fails_if_the_velocity_fields_shape_do_not_match_with_the_shape_of_the_time_vector(msh, U_vi, U_hi):
    """the initialization fails if the velocity fields shape do not match with the shape of the time vector"""
    with pytest.raises(ValueError) as e:
        t_fail = np.array([0])
        Velocity(msh, U_vi, U_hi, t=t_fail)
    assert e.type == ValueError


@then("the update fails if the time is not between the lowest and largest times contained in the time vector")
def the_update_fails_if_the_time_is_not_between_the_lowest_and_largest_times_contained_in_the_time_vector(U):
    """the update fails if the time is not between the lowest and largest times contained in the time vector"""
    with pytest.raises(ValueError) as e:
        U.at_current_time(max(U.t) + 1)
    assert e.type == ValueError
