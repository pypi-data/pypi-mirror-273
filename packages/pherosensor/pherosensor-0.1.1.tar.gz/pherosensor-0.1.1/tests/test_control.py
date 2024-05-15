from pathlib import Path

import numpy as np
import pytest
from pytest_bdd import given
from pytest_bdd import scenario
from pytest_bdd import then
from pytest_bdd import when

from pheromone_dispersion.geom import MeshRect2D
from pheromone_dispersion.source_term import Source
from pheromone_dispersion.velocity import Velocity
from source_localization.control import Control


@scenario("control.feature", "Generate the Control object")
def test_generate_the_Control_object():
    """Generate the Control object."""


@given("a rectangular 2D mesh", target_fixture="msh")
def a_rectangular_2D_mesh():
    "a rectangular 2D mesh"
    Lx = np.load(Path("tests/test_data") / "Lx.npy")
    Ly = np.load(Path("tests/test_data") / "Ly.npy")
    dx = np.load(Path("tests/test_data") / "dx.npy")
    dy = np.load(Path("tests/test_data") / "dy.npy")
    Tfinal = np.load(Path("tests/test_data") / "Tfinal.npy")
    msh = MeshRect2D(Lx, Ly, dx, dy, Tfinal - 1e-15)
    t = np.load(Path("tests/test_data") / "t.npy")
    U_vi = np.load(Path("tests/test_data") / "U_vi.npy")
    U_hi = np.load(Path("tests/test_data") / "U_hi.npy")
    U = Velocity(msh, U_vi, U_hi, t=t)
    msh.calc_dt_explicit_solver(U)
    return msh


@given("a source term", target_fixture="S")
def a_source_term(msh):
    "a source term"
    t = np.load(Path("tests/test_data") / "t.npy")
    Q = np.load(Path("tests/test_data") / "Q.npy")
    return Source(msh, Q, t=t)


@when("initialize the Control object", target_fixture='k')
def initialize_the_Control_object(msh, S):
    """initialize the Control object"""
    return Control(S, msh)


@then("check the array of the background values has the expected shape")
def check_the_array_of_the_background_values_has_the_expected_shape(msh, k):
    "check the array of the background values has the expected shape"
    assert k.background_value.shape == (msh.t_array.size * msh.x.size * msh.y.size,)


@then("check the array of the current values has the expected shape")
def check_the_array_of_the_current_values_has_the_expected_shape(msh, k):
    "check the array of the current values has the expected shape"
    assert k.value.shape == (msh.t_array.size * msh.x.size * msh.y.size,)


@then("check the array of the background values has the expected values")
def check_the_array_of_the_background_values_has_the_expected_values(msh, k):
    "check the array of the background values has the expected values"
    for i in range(msh.t_array.size):
        assert (k.background_value[i * msh.x.size * msh.y.size: (i + 1) * msh.x.size * msh.y.size] == 1.0 + i / 10).all


@then("check the array of the current values has the expected values")
def check_the_array_of_the_current_values_has_the_expected_values(msh, k):
    "check the array of the current values has the expected values"
    for i in range(msh.t_array.size):
        assert (k.value[i * msh.x.size * msh.y.size: (i + 1) * msh.x.size * msh.y.size] == 1.0 + i / 10).all


@then("the initialization fails if the time array is not initialized")
def the_initialization_fails_if_the_time_array_is_not_initialized(S):
    Lx = np.load(Path("tests/test_data") / "Lx.npy")
    Ly = np.load(Path("tests/test_data") / "Ly.npy")
    dx = np.load(Path("tests/test_data") / "dx.npy")
    dy = np.load(Path("tests/test_data") / "dy.npy")
    Tfinal = np.load(Path("tests/test_data") / "Tfinal.npy")
    msh = MeshRect2D(Lx, Ly, dx, dy, Tfinal - 1e-15)
    with pytest.raises(ValueError) as e:
        Control(S, msh)
    assert e.type == ValueError
