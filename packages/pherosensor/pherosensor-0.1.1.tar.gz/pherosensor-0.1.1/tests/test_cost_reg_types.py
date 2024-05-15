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


@scenario("cost_reg_types.feature", "test the list of types of regularization")
def test_the_list_of_types_of_regularization():
    """test the list of types of regularization."""


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


@when("generate the Cost object with no regularization", target_fixture="cost_no_reg")
def generate_the_Cost_object_with_no_regularization(msh, obs, ctrl):
    "generate the Cost object with no regularization"
    return Cost(msh, obs, ctrl, alpha=None, regularization_types=None)


@when("generate the Cost object with one regularization", target_fixture="cost_one_reg")
def generate_the_Cost_object_with_one_regularization(msh, obs, ctrl):
    "generate the Cost object with one regularization"
    return Cost(msh, obs, ctrl, alpha=0.75, regularization_types='Population dynamic')


@when("generate the Cost object with multiple regularizations", target_fixture="cost_multi_reg")
def generate_the_Cost_object_with_multiple_regularizations(msh, obs, ctrl):
    "generate the Cost object with multiple regularizations"
    regularization_types = ['Tikhonov', 'Stationnary population dynamic', 'LASSO']
    alpha = {'Tikhonov': 0.1, 'Stationnary population dynamic': 0.25, 'LASSO': 0.5}
    return Cost(msh, obs, ctrl, alpha=alpha, regularization_types=regularization_types)


@then("the attribute regularization_types is a list")
def the_attribute_regularization_types_is_a_list(cost_no_reg, cost_one_reg, cost_multi_reg):
    "the attribute regularization_types is a list"
    assert isinstance(cost_no_reg.regularization_types, list)
    assert isinstance(cost_one_reg.regularization_types, list)
    assert isinstance(cost_multi_reg.regularization_types, list)


@then("the attribute regularization_types has the expected value")
def the_attribute_regularization_types_has_the_expected_value(cost_no_reg, cost_one_reg, cost_multi_reg):
    "the attribute regularization_types has the expected value"
    assert cost_no_reg.regularization_types == []
    assert cost_one_reg.regularization_types == ['Population dynamic']
    assert cost_multi_reg.regularization_types == ['Tikhonov', 'Stationnary population dynamic', 'LASSO']


@then("input with wrong type raises exception")
def input_with_wrong_type_raises_exception(msh, obs, ctrl):
    "input with wrong type raises exception"
    regularization_type = {'invalide type': 'Population dynamic'}
    alpha = {'Population dynamic': 0.75}
    with pytest.raises(ValueError) as e:
        _ = Cost(msh, obs, ctrl, alpha=alpha, regularization_types=regularization_type)
    assert e.type == ValueError


@then("non string regularization type raises exception")
def non_float_weight_coefficient_raises_exception(msh, obs, ctrl):
    "non float weight coefficient raises exception"
    regularization_type = 0.1
    alpha = {'Population dynamic': 0.75}
    with pytest.raises(ValueError) as e:
        _ = Cost(msh, obs, ctrl, alpha=alpha, regularization_types=[regularization_type])
    assert e.type == ValueError


@then("not implemented regularization types raises exception")
def not_implemented_regularization_types_raises_exception(msh, obs, ctrl):
    "not implemented regularization types raises exception"
    alpha = {'Population dynamic': 0.75}
    with pytest.raises(ValueError) as e:
        _ = Cost(msh, obs, ctrl, alpha=alpha, regularization_types='invalid argument')
    assert e.type == ValueError
