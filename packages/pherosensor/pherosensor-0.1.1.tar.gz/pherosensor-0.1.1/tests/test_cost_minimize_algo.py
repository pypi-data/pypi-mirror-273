from pathlib import Path

import numpy as np
import pytest
from pytest_bdd import given
from pytest_bdd import scenario
from pytest_bdd import then
from pytest_bdd import when

from pheromone_dispersion.convection_diffusion_2D import DiffusionConvectionReaction2DEquation
from pheromone_dispersion.diffusion_tensor import DiffusionTensor
from pheromone_dispersion.geom import MeshRect2D
from pheromone_dispersion.source_term import Source
from pheromone_dispersion.velocity import Velocity
from source_localization.adjoint_convection_diffusion_2D import AdjointDiffusionConvectionReaction2DEquation
from source_localization.control import Control
from source_localization.cost import Cost
from source_localization.obs import Obs


@scenario("cost_minimize_algo.feature", "Test the call to the different optimization algorithm in the minimize method")
def test_minimize_algo():
    """Test the call to the different optimization algorithm in the minimize method."""


@given("a mesh", target_fixture="msh")
def a_mesh():
    "a mesh"
    Lx = np.load(Path("tests/test_data") / "Lx.npy")
    Ly = np.load(Path("tests/test_data") / "Ly.npy")
    dx = np.load(Path("tests/test_data") / "dx.npy")
    dy = np.load(Path("tests/test_data") / "dy.npy")
    Tfinal = np.load(Path("tests/test_data") / "Tfinal.npy")
    msh = MeshRect2D(Lx, Ly, dx, dy, Tfinal - 1e-15)
    return msh


@given("environmental parameters", target_fixture="env_param")
def environmental_parameters(msh):
    "environmental parameters"
    U_vi = np.load(Path("tests/test_data") / "U_vi.npy")
    U_hi = np.load(Path("tests/test_data") / "U_hi.npy")
    K_u = np.load(Path("tests/test_data") / "K_u.npy")
    K_ut = np.load(Path("tests/test_data") / "K_u_t.npy")
    env_param = {}
    env_param['t'] = np.load(Path("tests/test_data") / "t.npy")
    env_param['U'] = Velocity(msh, U_vi, U_hi, t=env_param['t'])
    env_param['K'] = DiffusionTensor(env_param['U'], K_u, K_ut)
    env_param['depot coeff'] = np.load(Path("tests/test_data") / "depot_coeff.npy")
    env_param['S'] = Source(msh, np.load(Path("tests/test_data") / "Q.npy"), t=env_param['t'])
    msh.calc_dt_explicit_solver(env_param['U'])
    return env_param


@given("a direct model", target_fixture="dm")
def a_direct_model(msh, env_param):
    "a direct model"
    return DiffusionConvectionReaction2DEquation(env_param['U'], env_param['K'], env_param['depot coeff'], env_param['S'], msh)


@given("observations", target_fixture="obs")
def observations(msh):
    "observations"
    t_obs = np.load(Path("tests/test_data") / "t_obs.npy")
    X = np.load(Path("tests/test_data") / "X_obs.npy")
    d = np.load(Path("tests/test_data") / "d_obs.npy")
    return Obs(t_obs, X, d, msh)


@given("an adjoint model", target_fixture="am")
def an_adjoint_model(msh, env_param):
    "an adjoint model"
    return AdjointDiffusionConvectionReaction2DEquation(
        env_param['U'], env_param['K'], env_param['depot coeff'], msh, time_discretization='implicit'
    )


@given("a control", target_fixture="ctrl")
def a_control(msh, env_param):
    "a control"
    ctrl = Control(env_param['S'], msh)
    ctrl.value = np.copy(ctrl.background_value)
    ctrl.background_value -= 1.0
    return ctrl


@when("intialize a cost with a differentiable regularization term", target_fixture="cost_diff")
def initialize_a_cost_with_a_differentiable_regularization_term(msh, obs, ctrl):
    "intialize a cost with a differentiable regularization term"
    return Cost(msh, obs, ctrl, alpha=0.5, regularization_types=['Tikhonov'])


@when("intialize a cost with a non differentiable regularization term", target_fixture="cost_non_diff")
def initialize_a_cost_with_a_non_differentiable_regularization_term(msh, obs, ctrl):
    "intialize a cost with a non differentiable regularization term"
    return Cost(msh, obs, ctrl, alpha=0.5, regularization_types=['LASSO'])


@then("minimizing a non differentiable function with the gradient descent algorithm raises exception")
def minimizing_a_non_differentiable_function_with_the_gradient_descent_algorithm_raises_exception(dm, am, cost_non_diff):
    "minimizing a non differentiable function with the gradient descent algorithm raises exception"
    with pytest.raises(ValueError) as e:
        _, _, _, _ = cost_non_diff.minimize(dm, am, 'gradient descent', options={})
    assert e.type == ValueError


@then("minimizing a non differentiable function with the L BFGS B algorithm raises exception")
def minimizing_a_non_differentiable_function_with_the_L_BFGS_B_algorithm_raises_exception(dm, am, cost_non_diff):
    "minimizing a non differentiable function with the L BFGS B algorithm raises exception"
    with pytest.raises(ValueError) as e:
        _, _, _, _ = cost_non_diff.minimize(dm, am, 'L-BFGS-B', options={})
    assert e.type == ValueError


@then("minimizing a differentiable function with the proximal gradient algorithm raises exception")
def minimizing_a_differentiable_function_with_the_proximal_gradient_algorithm_raises_exception(dm, am, cost_diff):
    "minimizing a differentiable function with the proximal gradient algorithm raises exception"
    with pytest.raises(ValueError) as e:
        _, _, _, _ = cost_diff.minimize(dm, am, 'proximal gradient', options={})
    assert e.type == ValueError


@then("minimizing with a non implemented algorithm raises exception")
def minimizing_with_a_non_implemented_algorithm_raises_exception(dm, am, cost_diff):
    "minimizing with a non implemented algorithm raises exception"
    with pytest.raises(ValueError) as e:
        _, _, _, _ = cost_diff.minimize(dm, am, 'not implemented', options={})
    assert e.type == ValueError
