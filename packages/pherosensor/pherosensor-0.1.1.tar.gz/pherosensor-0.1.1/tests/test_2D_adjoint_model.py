from pathlib import Path

import numpy as np
import pytest
from pytest_bdd import given
from pytest_bdd import scenario
from pytest_bdd import then
from pytest_bdd import when
from scipy.sparse.linalg import LinearOperator as LinOp

from pheromone_dispersion.advection_operator import Advection
from pheromone_dispersion.advection_operator import AdvectionAdjoint
from pheromone_dispersion.diffusion_operator import Diffusion
from pheromone_dispersion.diffusion_tensor import DiffusionTensor
from pheromone_dispersion.geom import MeshRect2D
from pheromone_dispersion.reaction_operator import Reaction
from pheromone_dispersion.source_term import Source
from pheromone_dispersion.velocity import Velocity
from source_localization.adjoint_convection_diffusion_2D import AdjointDiffusionConvectionReaction2DEquation
from source_localization.control import Control
from source_localization.cost import Cost
from source_localization.obs import Obs


@scenario("2D_adjoint_model.feature", "Generate the AdjointDiffusionConvectionReaction2DEquation object for the resolution of the PDE")
def test_generate_the_AdjointDiffusionConvectionReaction2DEquation_object():
    """Generate the AdjointDiffusionConvectionReaction2DEquation object for the resolution of the 2D PDE of the adjoint model."""


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
    U_vi = np.load(Path("tests/test_data") / "U_vi_non_zero_div.npy")
    U_hi = np.load(Path("tests/test_data") / "U_hi_non_zero_div.npy")
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


@given("observations", target_fixture="obs")
def observations(msh):
    "observations"
    t = np.load(Path("tests/test_data") / "t_obs.npy")
    X = np.load(Path("tests/test_data") / "X_obs.npy")
    d = np.load(Path("tests/test_data") / "d_obs.npy")
    obs = Obs(t, X, d, msh)
    obs.d_est = d + 1.0
    return obs


@given("cost", target_fixture="cost")
def cost(msh, obs):
    "cost"
    t = np.load(Path("tests/test_data") / "t.npy")
    Q = np.load(Path("tests/test_data") / "Q.npy")
    S = Source(msh, Q, t=t)
    ctrl = Control(S, msh)
    return Cost(msh, obs, ctrl)


@when("initialize the AdjointDiffusionConvectionReaction2DEquation object with semi implicit discretization", target_fixture='PDE_semi_imp')
def initialize_the_AdjointDiffusionConvectionReaction2DEquation_object_semi_implicit(U, K, depot_coeff, msh):
    """initialize the AdjointDiffusionConvectionReaction2DEquation object with semi implicit time discretization"""
    return AdjointDiffusionConvectionReaction2DEquation(U, K, depot_coeff, msh, time_discretization='semi-implicit')


@when("initialize the AdjointDiffusionConvectionReaction2DEquation object with implicit discretization", target_fixture='PDE_imp')
def initialize_the_AdjointDiffusionConvectionReaction2DEquation_object_implicit(U, K, depot_coeff, msh):
    """initialize the AdjointDiffusionConvectionReaction2DEquation object with implicit time discretization"""
    return AdjointDiffusionConvectionReaction2DEquation(U, K, depot_coeff, msh, time_discretization='implicit')


@then("the reaction term of the PDE is a linear operator")
def the_reaction_term_of_the_PDE_is_a_linear_operator(PDE_semi_imp, PDE_imp):
    """the reaction term of the PDE is a linear operator"""
    assert isinstance(PDE_semi_imp.R, LinOp) and isinstance(PDE_semi_imp.R, Reaction)
    assert isinstance(PDE_imp.R, LinOp) and isinstance(PDE_imp.R, Reaction)


@then("the diffusion term of the PDE is a linear operator")
def the_diffusion_term_of_the_PDE_is_a_linear_operator(PDE_semi_imp, PDE_imp):
    """the diffusion term of the PDE is a linear operator"""
    assert isinstance(PDE_semi_imp.D, LinOp) and isinstance(PDE_semi_imp.D, Diffusion)
    assert isinstance(PDE_imp.D, LinOp) and isinstance(PDE_imp.D, Diffusion)


@then("the convection term of the semi implicit PDE is a linear operator")
def the_convection_term_of_the_semi_implicit_PDE_is_a_linear_operator(PDE_semi_imp):
    """the convection term of the semi implicit PDE is a linear operator"""
    assert isinstance(PDE_semi_imp.negative_divU_advection_term, LinOp) and isinstance(PDE_semi_imp.negative_divU_advection_term, Reaction)
    assert isinstance(PDE_semi_imp.positive_divU_advection_term, LinOp) and isinstance(PDE_semi_imp.positive_divU_advection_term, Reaction)
    assert isinstance(PDE_semi_imp.A, LinOp) and isinstance(PDE_semi_imp.A, Advection)


@then("the div parts of the convection term of the semi implicit PDE have the expected values")
def the_div_parts_of_the_convection_term_of_the_semi_implicit_PDE_have_the_expected_values(PDE_semi_imp):
    """the div parts of the convection term of the semi implicit PDE have the expected values"""
    x = np.random.random((PDE_semi_imp.msh.y.shape[0] * PDE_semi_imp.msh.x.shape[0],))
    res_exp = PDE_semi_imp.positive_divU_advection_term(x)
    res_imp = PDE_semi_imp.negative_divU_advection_term(x)
    assert (res_exp == 2 * x).all()
    assert (res_imp == 0.0).all()


@then("the convection term of the implicit PDE is a linear operator")
def the_convection_term_of_the_implicit_PDE_is_a_linear_operator(PDE_imp):
    """the convection term of the implicit PDE is a linear operator"""
    assert isinstance(PDE_imp.A_adjoint, LinOp) and isinstance(PDE_imp.A_adjoint, AdvectionAdjoint)


@then("the output of the solver has the expected shape")
def the_output_of_the_solver_has_the_expected_shape(msh, cost, PDE_imp):
    """the output of the solver has the expected shape"""
    p = PDE_imp.solver(cost.obs.adjoint_derivative_obs_operator, cost, display_flag=False)
    assert p.shape == (msh.t_array.size * msh.y.size * msh.x.size,)


@then("the initialization fails if the given time discretization is not implemented")
def the_initialization_fails_if_the_given_time_discretization_is_not_implemented(U, K, depot_coeff, obs, msh):
    """the initialization fails if the given time discretization is not implemented"""
    with pytest.raises(ValueError) as e:
        AdjointDiffusionConvectionReaction2DEquation(U, K, depot_coeff, msh, time_discretization="not implemented")
    assert e.type == ValueError
