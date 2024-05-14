from pathlib import Path

import numpy as np
import pytest
from pytest_bdd import given
from pytest_bdd import scenario
from pytest_bdd import then
from pytest_bdd import when

from pheromone_dispersion.geom import MeshRect2D
from pheromone_dispersion.source_term import Source


@scenario("source_term.feature", "Generate the source term as a Source object")
def test_generate_the_source_term_as_a_Source_object():
    """Generate the source term as a Source object."""


@given("a time vector", target_fixture='t')
def a_time_vector():
    "a time vector"
    t = np.load(Path("tests/test_data") / "t.npy")
    return t


@given("a source term", target_fixture="Q")
def a_source_term():
    "a source term"
    Q = np.load(Path("tests/test_data") / "Q.npy")
    return Q


@given("an invalid source term", target_fixture="Q_invalid")
def an_invalid_source_term():
    "an invalid source term"
    Q = np.load(Path("tests/test_data") / "Q_invalid.npy")
    return Q


@given("a rectangular 2D mesh", target_fixture="msh")
def a_rectangular_2D_mesh():
    "a rectangular 2D mesh"
    Lx = np.load(Path("tests/test_data") / "Lx.npy")
    Ly = np.load(Path("tests/test_data") / "Ly.npy")
    dx = np.load(Path("tests/test_data") / "dx.npy")
    dy = np.load(Path("tests/test_data") / "dy.npy")
    Tfinal = np.load(Path("tests/test_data") / "Tfinal.npy")
    msh = MeshRect2D(Lx, Ly, dx, dy, Tfinal)
    return msh


@when("initialize the Source object", target_fixture='S')
def initialize_the_Source_object(t, msh, Q):
    """initialize the Source object"""
    return Source(msh, Q, t=t)


@when("initialize the steady Source object", target_fixture='S_steady')
def initialize_the_steady_Source_object(msh, Q):
    """initialize the steady Source object"""
    return Source(msh, Q[0, :, :])


@then("the source term has the expected value")
def the_source_term_has_the_expected_value(S):
    """the source term has the expected value"""
    assert (S.value == 1).all()


@then("the source term is correctly updated at a given time")
def the_source_term_is_correctly_updated_at_a_given_time(S):
    """the source term is correctly updated at a given time"""
    S.at_current_time(5 / 32)
    assert (S.value == 37 / 32).all()


@then("the update at a given time does not change the values")
def the_update_at_a_given_time_does_not_change_the_values(S_steady):
    """the update at a given time does not change the values"""
    S_save = np.copy(S_steady.value)
    S_steady.at_current_time(1.5)
    assert (S_save == S_steady.value).all()


@then("the initialization fails if the number of dimension of the source term is not correct")
def the_initialization_fails_if_the_number_of_dimension_of_the_source_term_is_not_correct(Q, t, msh):
    """the initialization fails if the number of dimension of the source term is not correct"""
    with pytest.raises(ValueError) as e:
        Source(msh, Q)
    assert e.type == ValueError
    with pytest.raises(ValueError) as e:
        Source(msh, Q[0, :, :], t=t)
    assert e.type == ValueError


@then("the initialization fails if the source term shape does not match the shape of the mesh")
def the_initialization_fails_if_the_source_term_shape_does_not_match_the_shape_of_the_mesh(Q_invalid, t, msh):
    """the initialization fails if the source term shape does not match the shape of the mesh"""
    with pytest.raises(ValueError) as e:
        Source(msh, Q_invalid)
    assert e.type == ValueError


@then("the initialization fails if the source term shape does not match the shape of the time array")
def the_initialization_fails_if_the_source_term_shape_does_not_match_the_shape_of_the_time_array(Q, t, msh):
    """the initialization fails if the source term shape does not match the shape of the time array"""
    with pytest.raises(ValueError) as e:
        Source(msh, Q[:-1, :, :], t=t)
    assert e.type == ValueError


@then("the update fails if the time is not between the lowest and largest times contained in the time vector")
def the_update_fails_if_the_time_is_not_between_the_lowest_and_largest_times_contained_in_the_time_vector(S):
    """the update fails if the time is not between the lowest and largest times contained in the time vector"""
    with pytest.raises(ValueError) as e:
        S.at_current_time(max(S.t) + 1)
    assert e.type == ValueError
