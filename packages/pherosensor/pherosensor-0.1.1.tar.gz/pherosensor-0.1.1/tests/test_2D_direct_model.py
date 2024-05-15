import os
from pathlib import Path

import numpy as np
import pytest
from pytest_bdd import given
from pytest_bdd import scenario
from pytest_bdd import then
from pytest_bdd import when
from scipy.sparse.linalg import LinearOperator as LinOp

from pheromone_dispersion.advection_operator import Advection
from pheromone_dispersion.convection_diffusion_2D import DiffusionConvectionReaction2DEquation
from pheromone_dispersion.diffusion_operator import Diffusion
from pheromone_dispersion.diffusion_tensor import DiffusionTensor
from pheromone_dispersion.geom import MeshRect2D
from pheromone_dispersion.reaction_operator import Reaction
from pheromone_dispersion.source_term import Source
from pheromone_dispersion.velocity import Velocity
from source_localization.obs import Obs


@scenario("2D_direct_model.feature", "Generate the DiffusionConvectionReaction2DEquation object for the resolution of the PDE")
def test_generate_the_DiffusionConvectionReaction2DEquation_object():
    """Generate the DiffusionConvectionReaction2DEquation object for the resolution of the 2D PDE of the direct model."""


@given("a rectangular 2D mesh", target_fixture="msh")
def a_rectangular_2D_mesh():
    "a rectangular 2D mesh"
    Lx = np.load(Path("tests/test_data") / "Lx.npy")
    Ly = np.load(Path("tests/test_data") / "Ly.npy")
    dx = np.load(Path("tests/test_data") / "dx.npy")
    dy = np.load(Path("tests/test_data") / "dy.npy")
    Tfinal = np.load(Path("tests/test_data") / "Tfinal.npy")
    msh = MeshRect2D(Lx, Ly, dx, dy, Tfinal - 1e-15)
    return msh


@given("a velocity field", target_fixture="U")
def a_velocity_field(msh):
    "a velocity field"
    t = np.load(Path("tests/test_data") / "t.npy")
    U_vi = np.load(Path("tests/test_data") / "U_vi.npy")
    U_hi = np.load(Path("tests/test_data") / "U_hi.npy")
    U = Velocity(msh, U_vi, U_hi, t=t)
    msh.calc_dt_explicit_solver(U)
    return U


@given("a diffusion tensor", target_fixture="K")
def a_diffusion_tensor(U):
    "a diffusion tensor"
    K_u = np.load(Path("tests/test_data") / "K_u.npy")
    K_ut = np.load(Path("tests/test_data") / "K_u_t.npy")
    return DiffusionTensor(U, K_u, K_ut)


@given("a deposition coefficient", target_fixture="depot_coeff")
def a_deposition_coefficient():
    "a deposition coefficient"
    depot_coeff = np.load(Path("tests/test_data") / "depot_coeff.npy")
    return depot_coeff


@given("a source term", target_fixture="Q")
def a_source_term(msh):
    "a source term"
    t = np.load(Path("tests/test_data") / "t.npy")
    Q = np.load(Path("tests/test_data") / "Q.npy")
    return Source(msh, Q, t=t)


@given("observations", target_fixture="obs")
def observations(msh):
    "observations"
    t = np.load(Path("tests/test_data") / "t_obs.npy")
    X = np.load(Path("tests/test_data") / "X_obs.npy")
    d = np.load(Path("tests/test_data") / "d_obs.npy")
    dt_obs_operator = msh.dt
    return Obs(t, X, d, msh, dt_obs_operator=dt_obs_operator)


@when("initialize the DiffusionConvectionReaction2DEquation object", target_fixture='PDE')
def initialize_the_DiffusionConvectionReaction2DEquation_object(U, K, depot_coeff, Q, msh):
    """initialize the DiffusionConvectionReaction2DEquation object"""
    return DiffusionConvectionReaction2DEquation(U, K, depot_coeff, Q, msh)


@when("the output are saved", target_fixture='C')
def the_output_are_saved(PDE, tmpdir):
    """the output are saved"""
    C = PDE.solver(save_all=True, path_save=tmpdir, display_flag=False)
    return C


@then("the reaction term of the PDE is a linear operator")
def the_reaction_term_of_the_PDE_is_a_linear_operator(PDE):
    """the reaction term of the PDE is a linear operator"""
    assert isinstance(PDE.R, LinOp) and isinstance(PDE.R, Reaction)


@then("the convection term of the PDE is a linear operator")
def the_convection_term_of_the_PDE_is_a_linear_operator(PDE):
    """the convection term of the PDE is a linear operator"""
    assert isinstance(PDE.A, LinOp) and isinstance(PDE.A, Advection)


@then("the diffusion term of the PDE is a linear operator")
def the_diffusion_term_of_the_PDE_is_a_linear_operator(PDE):
    """the diffusion term of the PDE is a linear operator"""
    assert isinstance(PDE.D, LinOp) and isinstance(PDE.D, Diffusion)


@then("check the output of the solver has the expected shape")
def check_the_output_of_the_solver_has_the_expected_shape(PDE, C):
    """check the output of the solver has the expected shape"""
    C_1TimeStep = PDE.solver_one_time_step(np.zeros((PDE.msh.y.shape[0], PDE.msh.x.shape[0])))
    assert C_1TimeStep.shape == (PDE.msh.y.size, PDE.msh.x.size)
    assert C.shape == (PDE.msh.t_array.size, PDE.msh.y.size, PDE.msh.x.size)


@then("the output directory exists")
def the_output_directory_exists(tmpdir):
    """the output directory exists"""
    assert os.path.isdir(tmpdir)


@then("the outputs are saved")
def the_outputs_are_saved(tmpdir):
    """the outputs are saved"""
    assert (Path(tmpdir) / 'c.npy').exists()


@then("the outputs have the expected shape")
def the_outputs_have_the_expected_shape(tmpdir, msh):
    """the outputs have the expected shape"""
    C_save = np.load(Path(tmpdir) / 'c.npy')
    assert C_save.shape == (msh.t_array.size, msh.y.size, msh.x.size)


@then("the saved outputs have the expected values")
def the_saved_outputs_have_the_expected_values(tmpdir, C):
    """the saved outputs have the expected values"""
    C_save = np.load(Path(tmpdir) / 'c.npy')
    assert (C_save == C).all()


@then("the solver at the observations times stores properly the estimation")
def the_solver_at_the_observations_times_stores_properly_the_estimation(msh, PDE, C, obs):
    "the solver at the observations times store properly the estimation"
    PDE.solver_est_at_obs_times(obs)
    truth = [
        [C[5, 2, 1], C[4, 2, 1]],
        [C[4, 1, 0], C[3, 1, 0]],
        [C[9, 2, 0], C[8, 2, 0]],
        [C[7, 0, 1], C[6, 0, 1]],
        [C[10, 1, 1], C[9, 1, 1]],
    ]
    assert (obs.c_est == truth).all()


@then("the initialization fails if the given time discretization is not implemented")
def the_initialization_fails_if_the_given_time_discretization_is_not_implemented(U, K, depot_coeff, Q, msh):
    """the initialization fails if the given time discretization is not implemented"""
    with pytest.raises(ValueError) as e:
        DiffusionConvectionReaction2DEquation(U, K, depot_coeff, Q, msh, time_discretization="not implemented")
    assert e.type == ValueError
