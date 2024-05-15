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


@scenario("cost_reg.feature", "Compute the regularization terms of the cost function and its gradients")
def test_compute_reg_costs():
    """Compute the regularization terms of the cost function and its gradients."""


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
    ctrl = Control(S, msh, population_dynamique_death_rate=.1)
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


@when("compute the cost")
def compute_the_cost(cost_no_reg, cost_one_reg, cost_multi_reg):
    "compute the cost"
    cost_no_reg.reg_cost()
    cost_one_reg.reg_cost()
    cost_multi_reg.obs.d_est = cost_multi_reg.obs.d_obs + 1.0
    cost_multi_reg.objectif()


@then("the attribute j_reg is a dict")
def the_attribute_j_reg_is_a_dict(cost_no_reg, cost_one_reg, cost_multi_reg):
    "the attribute j_reg is a dict"
    assert isinstance(cost_no_reg.j_reg, dict)
    assert isinstance(cost_one_reg.j_reg, dict)
    assert isinstance(cost_multi_reg.j_reg, dict)


@then("the cost has the expected value")
def the_cost_has_the_expected_value(cost_no_reg, cost_one_reg, cost_multi_reg):
    "the cost has the expected value"

    assert cost_no_reg.j_reg == {}

    true_j_reg_PDB = 13.3485 * cost_no_reg.msh.L_x * cost_no_reg.msh.L_y * cost_no_reg.msh.dt * 0.75
    assert np.abs(cost_one_reg.j_reg['Population dynamic'] - true_j_reg_PDB) < 2*1e-15

    true_j_obs = cost_no_reg.msh.mass_cell * cost_no_reg.msh.dt * 5
    true_j_reg_T = 0.1 * cost_no_reg.msh.L_x * cost_no_reg.msh.L_y * (cost_no_reg.msh.T_final + cost_no_reg.msh.dt)
    true_j_reg_SPDB = 0.25 * cost_no_reg.msh.L_x * cost_no_reg.msh.L_y * cost_no_reg.msh.T_final
    true_j_reg_LASSO = 0.5 * cost_no_reg.msh.L_x * cost_no_reg.msh.L_y * 16.5 * cost_no_reg.msh.dt
    assert len(cost_multi_reg.j_reg) == 3
    assert cost_multi_reg.j_reg['Tikhonov'] == true_j_reg_T
    assert np.abs(cost_multi_reg.j_reg['Stationnary population dynamic'] - true_j_reg_SPDB) < 1e-15
    assert cost_multi_reg.j_reg['LASSO'] == true_j_reg_LASSO
    assert cost_multi_reg.j == true_j_obs + true_j_reg_T + true_j_reg_SPDB + true_j_reg_LASSO


@then("the gradients have the expected values and shape")
def the_gradients_have_the_expected_values_and_shape(msh, cost_no_reg, cost_multi_reg):
    "the gradients have the expected values and shape"
    gradient_objectif_wrt_S_no_reg = cost_no_reg.gradient_objectif_wrt_S()
    gradient_objectif_wrt_S = cost_multi_reg.gradient_objectif_wrt_S()

    grad_reg_SPDB = np.zeros((msh.t_array.size, msh.y.size, msh.x.size))
    grad_reg_SPDB[0, :, :] = -0.1 * cost_multi_reg.alpha['Stationnary population dynamic'] * 2 / msh.dt**2
    grad_reg_SPDB[-1, :, :] = 0.1 * cost_multi_reg.alpha['Stationnary population dynamic'] * 2 / msh.dt**2
    grad_reg_T = cost_multi_reg.alpha['Tikhonov'] * 2 * np.ones((msh.t_array.size, msh.y.size, msh.x.size))
    gradient_objectif_wrt_S_true = (grad_reg_SPDB + grad_reg_T).reshape((msh.t_array.size * msh.y.size * msh.x.size,))
    assert gradient_objectif_wrt_S.shape == cost_multi_reg.ctrl.value.shape
    assert (np.abs(gradient_objectif_wrt_S - gradient_objectif_wrt_S_true) < 2 * 1e-14).all()
    assert (gradient_objectif_wrt_S_no_reg == 0.0).all()


@then("the proximal operator have the expected values and shape")
def the_proximal_operator_have_the_expected_values_and_shape(cost_multi_reg):
    "the proximal operator have the expected values and shape"
    x = np.arange(-6, 6, 1) * 0.1
    lam = 9
    prox = cost_multi_reg.reg_proximal_operator(x, lam)
    prox_true = np.array([-1.5, -0.5, -0.0, -0.0, -0.0, -0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5]) * 0.1
    assert (np.abs(prox - prox_true) < 1e-16).all()


@then("computing the proximal operator for differentiable regularization term raises exception")
def computing_the_proximal_operator_for_differentiable_regularization_term_raises_exception(cost_no_reg):
    """computing the proximal operator for differentiable regularization term raises exception"""
    x = np.arange(-6, 6, 1)
    lam = 9
    with pytest.raises(ValueError) as e:
        _ = cost_no_reg.reg_proximal_operator(x, lam)
    assert e.type == ValueError
