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


@scenario("cost_remove_reg.feature", "Test the method to remove regularization term to the cost function")
def Test_the_method_to_remove_regularization_term_to_the_cost_function():
    """Test the method to remove regularization term to the cost function."""


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
    alpha = {'Tikhonov': 0.5, 'Population dynamic': 0.1}
    regularization_types = ['Tikhonov', 'Population dynamic']
    return Cost(msh, obs, ctrl, alpha=alpha, regularization_types=regularization_types)


@when("remove a regularization term")
def remove_a_regularization_term(cost):
    "remove a regularization term"
    cost.remove_reg('Tikhonov')


@when("remove a regularization term not considered")
def remove_a_regularization_term_not_considered(cost):
    "remove a regularization term not considered"
    cost.remove_reg('not considered')


@then("the attribute regularization_types is correctly updated")
def the_attribute_regularization_types_is_correctly_updated(cost):
    "the attribute regularization_types is correctly updated"
    assert cost.regularization_types == ['Population dynamic']


@then("the attribute alpha is correctly updated")
def the_attribute_alpha_is_correctly_updated(cost):
    "the attribute alpha is correctly updated"
    assert cost.alpha == {'Population dynamic': 0.1}


@then("the attribute j_reg is correctly updated")
def the_attribute_j_reg_is_correctly_updated(cost):
    "the attribute j_reg is correctly updated"
    assert cost.j_reg == {'Population dynamic': 0.0}


@then("removing a regularization term not implemented raises exception")
def removing_a_regularization_term_not_implemented_raises_exception(cost):
    "removing a regularization term not implemented raises exception"
    with pytest.raises(ValueError) as e:
        cost.remove_reg('not implemented')
    assert e.type == ValueError
