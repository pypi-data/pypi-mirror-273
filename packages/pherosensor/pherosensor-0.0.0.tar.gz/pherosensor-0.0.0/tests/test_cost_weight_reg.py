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


@scenario("cost_weight_reg.feature", "test the dictionnary containing the weight coefficients of the regularization terms")
def test_the_dictionnary_containing_the_weight_coefficients_of_the_regularization_terms():
    """test the dictionnary containing the weight coefficients of the regularization terms."""


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
    regularization_types = ['Tikhonov', 'Stationnary population dynamic', 'LASSO', 'Population dynamic']
    alpha = {'Tikhonov': 0.1, 'Stationnary population dynamic': 0.25, 'LASSO': 0.5, 'Population dynamic': 0.0}
    return Cost(msh, obs, ctrl, alpha=alpha, regularization_types=regularization_types)


@then("the attribute alpha is a dict")
def the_attribute_alpha_is_a_dict(cost_no_reg, cost_one_reg, cost_multi_reg):
    "the attribute alpha is a dict"
    assert isinstance(cost_no_reg.alpha, dict)
    assert isinstance(cost_one_reg.alpha, dict)
    assert isinstance(cost_multi_reg.alpha, dict)


@then("the attribute alpha has the expected value")
def the_attribute_alpha_has_the_expected_value(cost_no_reg, cost_one_reg, cost_multi_reg):
    "the attribute alpha has the expected value"
    assert cost_no_reg.alpha == {}
    assert cost_one_reg.alpha == {'Population dynamic': 0.75}
    assert cost_multi_reg.alpha == {'Tikhonov': 0.1, 'Stationnary population dynamic': 0.25, 'LASSO': 0.5}


@then("input with wrong type raises exception")
def input_alpha_with_wrong_type_raises_exception(msh, obs, ctrl):
    "input alpha with wrong type raises exception"
    regularization_types = ['Population dynamic']
    alpha = 0.75
    with pytest.raises(ValueError) as e:
        _ = Cost(msh, obs, ctrl, alpha=[alpha], regularization_types=regularization_types)
    assert e.type == ValueError


@then("non float weight coefficient raises exception")
def non_float_weight_coefficient_raises_exception(msh, obs, ctrl):
    "non float weight coefficient raises exception"
    regularization_types = ['Population dynamic']
    alpha = 'invalid'
    with pytest.raises(ValueError) as e:
        _ = Cost(msh, obs, ctrl, alpha={regularization_types[0]: alpha}, regularization_types=regularization_types)
    assert e.type == ValueError


@then("different number of element in list of reg types and dict of weight coeff raises exception")
def different_number_of_element_in_list_of_reg_types_and_dict_weight_coeff_raises_exception(msh, obs, ctrl):
    "different number of element in list of regularization types and dict of weight coefficients raises exception"
    regularization_types = []
    alpha = {'Population dynamic': 0.75}
    with pytest.raises(ValueError) as e:
        _ = Cost(msh, obs, ctrl, alpha=alpha, regularization_types=regularization_types)
    assert e.type == ValueError

    regularization_types = ['Tikhonov', 'Stationnary population dynamic']
    alpha = {'Tikhonov': 0.1, 'Stationnary population dynamic': 0.25, 'LASSO': 0.5}
    with pytest.raises(ValueError) as e:
        _ = Cost(msh, obs, ctrl, alpha={regularization_types[0]: alpha}, regularization_types=regularization_types)
    assert e.type == ValueError


@then("difference between list of reg types and keys of dict of weight coeff raises exception")
def difference_between_list_of_reg_types_and_keys_dict_weight_coeff_raises_exception(msh, obs, ctrl):
    "difference between list of regularization types and keys of dict of weight coefficients raises exception"
    regularization_types = ['Tikhonov', 'Stationnary population dynamic', 'LASSO']
    alpha = {'Tikhonov': 0.1, 'Stationnary population dynamic': 0.25, 'Population dynamic': 0.5}
    with pytest.raises(ValueError) as e:
        _ = Cost(msh, obs, ctrl, alpha={regularization_types[0]: alpha}, regularization_types=regularization_types)
    assert e.type == ValueError
