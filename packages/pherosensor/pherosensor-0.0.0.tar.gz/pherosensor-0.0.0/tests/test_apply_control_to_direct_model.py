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
from source_localization.control import Control


@scenario("apply_control_to_direct_model.feature", "Apply the control to the direct model")
def test_apply_control_to_direct_model():
    """Apply the control to the direct model."""


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


@given("a control", target_fixture="k")
def a_control(msh):
    "a control"
    t = np.load(Path("tests/test_data") / "t.npy")
    Q = np.load(Path("tests/test_data") / "Q.npy")
    S = Source(msh, Q, t=t)
    return Control(S, msh)


@given("a direct model", target_fixture="direct_model")
def a_direct_model(msh):
    "a direct model"
    t = np.load(Path("tests/test_data") / "t.npy")

    U_vi = np.load(Path("tests/test_data") / "U_vi.npy")
    U_hi = np.load(Path("tests/test_data") / "U_hi.npy")
    U = Velocity(msh, U_vi, U_hi, t=t)

    K_u = np.load(Path("tests/test_data") / "K_u.npy")
    K_ut = np.load(Path("tests/test_data") / "K_u_t.npy")
    K = DiffusionTensor(U, K_u, K_ut)

    depot_coeff = np.load(Path("tests/test_data") / "depot_coeff.npy")

    Q = np.load(Path("tests/test_data") / "Q.npy")
    S = Source(msh, Q[1, :, :])

    return DiffusionConvectionReaction2DEquation(U, K, depot_coeff, S, msh)


@when("apply the control to the direct model")
def apply_the_control_to_the_direct_model(k, direct_model):
    "apply the control to the direct model"
    k.apply_control(direct_model)


@then("check the source term of the direct model has the expected value")
def check_the_source_term_of_the_direct_model_has_the_expected_value(msh, direct_model):
    "check the source term of the direct model has the expected value"
    assert (direct_model.S.t == msh.t_array).all()
    assert (direct_model.S.value == 1.0).all
