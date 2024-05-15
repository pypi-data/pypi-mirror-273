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


@scenario("cost_modify_weight_reg.feature", "Test the method to modify the weight of a regularization term")
def test_the_method_to_modify_the_weight_of_a_regularization_term():
    """test the method to modify the weight of a regularization term."""


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


@given("a cost function", target_fixture="cost")
def a_cost_function(msh, obs, ctrl):
    "a cost function"
    alpha = {'Tikhonov': 0.5, 'Population dynamic': 0.1, 'LASSO': 0.25}
    regularization_types = ['Tikhonov', 'Population dynamic', 'LASSO']
    return Cost(msh, obs, ctrl, alpha=alpha, regularization_types=regularization_types)


@when("modify a weight coefficient")
def modify_a_weight_coefficient(cost):
    "modify a weight coefficient"
    cost.modify_weight_reg('LASSO', 0.5)


@when("set a weight coefficient to 0")
def set_a_weight_coefficient_to_0(cost):
    "set a weight coefficient to 0"
    cost.modify_weight_reg('Population dynamic', 0.0)


@then("the attribute alpha is correctly updated")
def the_attribute_alpha_is_correctly_updated(cost):
    "the attribute alpha is correctly updated"
    assert cost.alpha == {'Tikhonov': 0.5, 'LASSO': 0.5}


@then("modifying a regularization term not implemented raises exception")
def modifying_a_regularization_term_not_implemented_raises_exception(cost):
    "modifying a regularization term not implemented raises exception"
    with pytest.raises(ValueError) as e:
        cost.modify_weight_reg('not implemented', 0.25)
    assert e.type == ValueError


@then("modifying a regularization term not considered raises exception")
def modifying_regularization_term_not_considered_raises_exception(cost):
    "modifying a regularization term not considered raises exception"
    with pytest.raises(ValueError) as e:
        cost.modify_weight_reg('Stationnary population dynamic', 0.25)
    assert e.type == ValueError
