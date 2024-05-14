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
from source_localization.cost import Cost
from source_localization.obs import Obs


@scenario("cost.feature", "Generate the Cost object and compute the cost function")
def test_generate_Cost_object():
    """Generate the Cost object and compute the cost function."""


@given("a mesh", target_fixture="msh")
def a_mesh():
    "a mesh"
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


@given("observations", target_fixture="obs")
def observations(msh):
    "observations"
    t = np.load(Path("tests/test_data") / "t_obs.npy")
    X = np.load(Path("tests/test_data") / "X_obs.npy")
    d = np.load(Path("tests/test_data") / "d_obs.npy")
    return Obs(t, X, d, msh)


@given("a control", target_fixture="ctrl")
def a_control(msh):
    "a control"
    t = np.load(Path("tests/test_data") / "t.npy")
    Q = np.load(Path("tests/test_data") / "Q.npy")
    S = Source(msh, Q, t=t)
    ctrl = Control(S, msh)
    ctrl.value = np.copy(ctrl.background_value)
    ctrl.background_value -= 1.0
    return ctrl


@when("generate the Cost object", target_fixture="cost")
def generate_the_Cost_object(msh, obs, ctrl):
    "generate the Cost object"
    return Cost(msh, obs, ctrl, alpha=0.5, regularization_types='Tikhonov')


@when("compute the cost")
def compute_the_cost(cost):
    "compute the cost"
    d_prov = np.load(Path("tests/test_data") / "d_obs.npy")
    cost.obs.d_est = d_prov + 1.0
    cost.objectif()


@then("the cost is a float")
def the_cost_is_a_float(cost):
    "the cost is a float"
    assert isinstance(cost.j, float)


@then("the cost has the expected value")
def the_cost_has_the_expected_value(cost):
    "the cost has the expected value"
    true_j_obs = cost.msh.mass_cell * cost.msh.dt * 5
    true_j_reg = 0.5 * cost.msh.L_x * cost.msh.L_y * (cost.msh.T_final + cost.msh.dt)
    assert cost.j == true_j_obs + true_j_reg


@then("Computing the cost without estimating the observed variable raises exception")
def computing_the_cost_without_estimating_the_observed_variable_raises_exception(msh, ctrl):
    "Computing the cost without estimating the observed variable raises exception"
    t = np.load(Path("tests/test_data") / "t_obs.npy")
    X = np.load(Path("tests/test_data") / "X_obs.npy")
    d = np.load(Path("tests/test_data") / "d_obs.npy")
    obs_fail = Obs(t, X, d, msh)
    j = Cost(msh, obs_fail, ctrl)
    with pytest.raises(ValueError) as e:
        j.objectif()
    assert e.type == ValueError
