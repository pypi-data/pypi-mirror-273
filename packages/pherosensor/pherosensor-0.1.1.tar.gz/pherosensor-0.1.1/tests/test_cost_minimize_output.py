import os
from pathlib import Path

import numpy as np
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


@scenario("cost_minimize_output.feature", "Test the outputs of the minimize method")
def test_minimize_output():
    """Test the outputs of the minimize method."""


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


@given("a maximum number of optimization iteration", target_fixture="nb_iter")
def a_maximum_number_of_optimization_iteration():
    "a maximum number of optimization iteration"
    return 5


@when("intialize a cost", target_fixture="cost")
def intialize_a_cost(msh, obs, ctrl):
    "intialize a cost"
    regularization_types = ['Tikhonov', 'Stationnary population dynamic']
    alpha = {'Tikhonov': 0.5, 'Stationnary population dynamic': 0.5}
    return Cost(msh, obs, ctrl, alpha=alpha, regularization_types=regularization_types)


@when("the cost function is minimized and the outputs saved", target_fixture="output")
def the_cost_function_is_minimized_and_the_outputs_saved(dm, am, nb_iter, cost, tmpdir):
    "the differentiable cost function is minimized"
    options = {'ftol': 1e-16, 'gtol': 1e-16, 'nit_max': nb_iter, "step size": 0.000001}
    dm, j_obs_vs_ite, j_reg_vs_ite, S_a = cost.minimize(dm, am, 'gradient descent', options=options, path_save=tmpdir)
    output = {
        'j_obs_vs_ite': j_obs_vs_ite,
        'S_a': S_a,
        'j_reg_vs_ite_T': j_reg_vs_ite['Tikhonov'],
        'alpha_T': cost.alpha['Tikhonov'],
        'j_reg_vs_ite_SPD': j_reg_vs_ite['Stationnary population dynamic'],
        'alpha_SPD': cost.alpha['Stationnary population dynamic'],
    }
    return output


@then("the outputs have the expected type")
def the_outputs_have_the_expected_type(output):
    "the outputs have the expected type"
    assert isinstance(output['j_obs_vs_ite'], list)
    assert isinstance(output['j_reg_vs_ite_T'], list)
    assert isinstance(output['j_reg_vs_ite_SPD'], list)
    assert isinstance(output['S_a'], np.ndarray)
    for j_obs, j_reg_T, j_reg_SPD in zip(
        output['j_obs_vs_ite'], output['j_reg_vs_ite_T'], output['j_reg_vs_ite_SPD']
    ):
        assert isinstance(j_obs, float)
        assert isinstance(j_reg_T, float)
        assert isinstance(j_reg_SPD, float)


@then("the outputs have the expected size")
def the_outputs_have_the_expected_size(msh, nb_iter, output):
    "the outputs have the expected size"
    assert len(output['j_obs_vs_ite']) == nb_iter
    assert len(output['j_reg_vs_ite_T']) == nb_iter
    assert len(output['j_reg_vs_ite_SPD']) == nb_iter
    assert output['S_a'].size == (msh.t_array.size * msh.y.size * msh.x.size)


@then("the value of the control has been updated")
def the_value_of_the_control_has_been_updated(msh, cost, output):
    "the value of the control has been updated"
    assert (cost.ctrl.value == output['S_a']).all()


@then("the output directory and files exist")
def the_output_directory_and_files_exist(tmpdir):
    "the output directory and files exist"
    assert os.path.isdir(tmpdir)
    assert (Path(tmpdir) / 'alpha_Tikhonov.npy').exists()
    assert (Path(tmpdir) / 'alpha_Stationnary_population_dynamic.npy').exists()
    assert (Path(tmpdir) / 'S_optim.npy').exists()
    assert (Path(tmpdir) / 'j_obs_vs_ite.npy').exists()
    assert (Path(tmpdir) / 'j_reg_Tikhonov_vs_ite.npy').exists()
    assert (Path(tmpdir) / 'j_reg_Stationnary_population_dynamic_vs_ite.npy').exists()


@then("the saved output have the expected values")
def the_saved_output_have_the_expected_values(tmpdir, output):
    "the saved output have the expected values"
    alpha_save_T = np.load((Path(tmpdir) / 'alpha_Tikhonov.npy'))
    alpha_save_SPD = np.load((Path(tmpdir) / 'alpha_Stationnary_population_dynamic.npy'))
    S_a_save = list(np.load((Path(tmpdir) / 'S_optim.npy')))
    j_obs_vs_ite_save = np.load((Path(tmpdir) / 'j_obs_vs_ite.npy')).tolist()
    j_reg_vs_ite_save_T = np.load((Path(tmpdir) / 'j_reg_Tikhonov_vs_ite.npy')).tolist()
    j_reg_vs_ite_save_SPD = np.load((Path(tmpdir) / 'j_reg_Stationnary_population_dynamic_vs_ite.npy')).tolist()
    assert alpha_save_T == output['alpha_T']
    assert alpha_save_SPD == output['alpha_SPD']
    assert (S_a_save == output['S_a']).all()
    assert j_obs_vs_ite_save == output['j_obs_vs_ite']
    assert j_reg_vs_ite_save_T == output['j_reg_vs_ite_T']
    assert j_reg_vs_ite_save_SPD == output['j_reg_vs_ite_SPD']
