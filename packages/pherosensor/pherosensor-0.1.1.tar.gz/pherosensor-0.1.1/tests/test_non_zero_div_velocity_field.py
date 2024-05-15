from pathlib import Path

import numpy as np
from pytest_bdd import given
from pytest_bdd import scenario
from pytest_bdd import then
from pytest_bdd import when

from pheromone_dispersion.geom import MeshRect2D
from pheromone_dispersion.velocity import Velocity


@scenario("non_zero_div_velocity_field.feature", "Generate the non-zero deivergence velocity field as a velocity object")
def test_generate_non_zero_divergence_velocity_field_as_velocity_object():
    """Generate the non-zero deivergence velocity field as a velocity object."""


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
    U_vi = np.load(Path("tests/test_data") / "U_vi_non_zero_div.npy")
    return U_vi


@given("a velocity field at the horizontal interfaces", target_fixture='U_hi')
def a_velocity_field_at_the_horizontal_interfaces():
    "a velocity field at the horizontal interfaces"
    U_hi = np.load(Path("tests/test_data") / "U_hi_non_zero_div.npy")
    return U_hi


@when("initialize the velocity object", target_fixture='U')
def initialize_the_velocity_object(msh, t, U_vi, U_hi):
    """initialize the velocity object"""
    return Velocity(msh, U_vi, U_hi, t=t)


@then("the matrix of the divergence of the velocity field has the expected shape")
def the_matrix_of_the_divergence_of_the_velocity_field_has_the_expected_shape(U):
    """the matrix of the divergence of the velocity field has the expected shape"""
    assert U.div.shape == (3, 2)


@then("the matrix of the divergence of the velocity field has the expected values")
def the_matrix_of_the_divergence_of_the_velocity_field_has_the_expected_values(U):
    """the matrix of the divergence of the velocity field has the expected values"""
    assert (U.div == 2).all()


@then("the divergence of the velocity field is correctly updated at a given time")
def the_divergence_of_the_velocity_field_is_correctly_updated_at_a_given_time(U):
    """the divergence of the velocity field is correctly updated at a given time"""
    U.at_current_time(1 / 2)
    assert (U.div == 1).all()
