import os
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


@scenario("cost_minimize_restart.feature", "Test the restart process of the minimize method")
def test_minimize_restart():
    """Test the restart process of the minimize method."""


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


@given("a cost function", target_fixture="cost")
def a_cost_function(msh, obs, ctrl):
    "a cost function"
    return Cost(msh, obs, ctrl, alpha=0.5, regularization_types=['Tikhonov'])


@given("a maximum number of optimization iteration", target_fixture="nb_iter")
def a_maximum_number_of_optimization_iteration():
    "a maximum number of optimization iteration"
    return 5


@when("the cost is minimized at one go", target_fixture="output_one_go")
def the_cost_is_minimized_at_one_go(dm, am, nb_iter, cost):
    "the cost is minimized at one go"
    options = {'ftol': 1e-16, 'gtol': 1e-16, 'nit_max': nb_iter, "step size": 0.000001}
    dm, j_obs_vs_ite, j_reg_vs_ite, S_vs_ite = cost.minimize(dm, am, 'gradient descent', options=options)
    output = {}
    output['dm'] = dm
    output['j_obs_vs_ite'] = j_obs_vs_ite
    output['j_reg_vs_ite'] = j_reg_vs_ite['Tikhonov']
    output['S_vs_ite'] = S_vs_ite
    output['alpha'] = cost.alpha['Tikhonov']
    return output


@when("the cost is minimized with a restart", target_fixture="output_restart")
def the_cost_is_minimized_with_a_restart(dm, am, nb_iter, cost, tmpdir):
    "the cost is minimized at one go"
    options_1 = {'ftol': 1e-16, 'gtol': 1e-16, 'nit_max': nb_iter - (nb_iter // 2), "step size": 0.000001}
    dm_1, j_obs_vs_ite_1, j_reg_vs_ite_1, S_vs_ite_1 = cost.minimize(dm, am, 'gradient descent', options=options_1, path_save=tmpdir)
    options_2 = {'ftol': 1e-16, 'gtol': 1e-16, 'nit_max': nb_iter // 2, "step size": 0.000001}
    dm_2, j_obs_vs_ite_2, j_reg_vs_ite_2, S_vs_ite_2 = cost.minimize(
        dm, am, 'gradient descent', options=options_2, path_save=tmpdir, restart_flag=True
    )
    output = {}
    output['j_obs_vs_ite'] = j_obs_vs_ite_2
    output['j_reg_vs_ite'] = j_reg_vs_ite_2['Tikhonov']
    output['S_vs_ite'] = S_vs_ite_2
    return output


@then("the outputs of the optimization with restart have the expected values")
def the_outputs_of_the_optimization_with_restart_have_the_expected_values(output_one_go, output_restart):
    "the outputs of the optimization with restart have the expected values"

    for S_one_go, S_restart in zip(output_one_go['S_vs_ite'], output_restart['S_vs_ite']):
        assert (S_restart == S_one_go).all()
    assert output_one_go['j_obs_vs_ite'] == output_restart['j_obs_vs_ite']
    assert output_one_go['j_reg_vs_ite'] == output_restart['j_reg_vs_ite']


@then("restarting optimization with an invalid directory raises exception")
def restarting_optimization_with_an_invalid_directory_raises_exception(dm, am, nb_iter, cost):
    "restarting optimization with an invalid directory raises exception"
    options = {'ftol': 1e-16, 'gtol': 1e-16, 'nit_max': nb_iter // 2, "step size": 0.000001}
    fail_dir = Path('/fail')
    with pytest.raises(ValueError) as e:
        _, _, _, _ = cost.minimize(dm, am, 'gradient descent', options=options, path_save=fail_dir, restart_flag=True)
    assert e.type == ValueError


@then("restarting optimization with missing files in the directory raises exception")
def restarting_optimization_with_missing_files_in_the_directory_raises_exception(tmpdir, dm, am, nb_iter, cost):
    "restarting optimization with missing files in the directory raises exceptions"
    options = {'ftol': 1e-16, 'gtol': 1e-16, 'nit_max': nb_iter // 2, "step size": 0.000001}
    fail_dir = Path(tmpdir) / 'no_files'
    os.makedirs(fail_dir)
    with pytest.raises(ValueError) as e:
        _, _, _, _ = cost.minimize(dm, am, 'gradient descent', options=options, path_save=fail_dir, restart_flag=True)
    assert e.type == ValueError
