from pathlib import Path

import numpy as np
from pytest_bdd import given
from pytest_bdd import scenario
from pytest_bdd import then
from pytest_bdd import when
from scipy.sparse.linalg import LinearOperator as LinOp

from pheromone_dispersion.diffusion_operator import Diffusion
from pheromone_dispersion.diffusion_tensor import DiffusionTensor
from pheromone_dispersion.geom import MeshRect2D
from pheromone_dispersion.velocity import Velocity


@scenario("diffusion_term.feature", "Generate the diffusion term of the convection-diffusion PDE as a linear operator")
def test_generate_diffusion_term_as_linear_operator():
    """Generate the diffusion term of the convection-diffusion PDE as a linear operator."""


@given("a rectangular 2D mesh", target_fixture="msh")
def a_rectangular_2D_mesh():
    "a rectangular 2D mesh"
    Lx = np.load(Path("tests/test_data") / "Lx.npy")
    Ly = np.load(Path("tests/test_data") / "Ly.npy")
    dx = np.load(Path("tests/test_data") / "dx.npy")
    dy = np.load(Path("tests/test_data") / "dy.npy")
    Tfinal = np.load(Path("tests/test_data") / "Tfinal.npy")
    return MeshRect2D(Lx, Ly, dx, dy, Tfinal)


@given("a diffusion tensor", target_fixture="K")
def a_diffusion_tensor(msh):
    "a diffusion tensor"
    "The diffusion tensor is isotropic for now"
    t = np.load(Path("tests/test_data") / "t.npy")
    U_vi = np.load(Path("tests/test_data") / "U_vi.npy")
    U_hi = np.load(Path("tests/test_data") / "U_hi.npy")
    K_u = np.load(Path("tests/test_data") / "K_u.npy")
    # K_ut = np.load(Path("tests/test_data") / "K_u_t.npy")
    return DiffusionTensor(Velocity(msh, U_vi, U_hi, t=t), K_u, K_u)


@given("a steady diffusion tensor", target_fixture="K_steady")
def a_steady_diffusion_tensor(msh):
    "a steady diffusion tensor"
    "The diffusion tensor is isotropic for now"
    U_vi = np.load(Path("tests/test_data") / "U_vi.npy")[0, :, :, :]
    U_hi = np.load(Path("tests/test_data") / "U_hi.npy")[0, :, :, :]
    K_u = np.load(Path("tests/test_data") / "K_u.npy")
    # K_ut = np.load(Path("tests/test_data") / "K_u_t.npy")
    return DiffusionTensor(Velocity(msh, U_vi, U_hi), K_u, K_u)


@when("initialize the diffusion linear operator", target_fixture='diffusion')
def initialize_the_diffusion_linear_operator(K, msh):
    """initialize the diffusion linear operator"""
    return Diffusion(K, msh)


@when("initialize the steady diffusion linear operator", target_fixture='diffusion_steady')
def initialize_the_steady_diffusion_linear_operator(K_steady, msh):
    """initialize the steady diffusion linear operator"""
    return Diffusion(K_steady, msh)


@then("the diffusion term is a linear operator")
def the_diffusion_term_is_a_linear_operator(diffusion):
    """the diffusion term is a linear operator"""
    assert issubclass(Diffusion, LinOp) and isinstance(diffusion, LinOp)


@then("the result of the matrice vector product of the linear operator has the expected shape")
def the_result_of_the_matrice_vector_product_of_the_linear_operator_has_the_expected_shape(msh, diffusion):
    """the result of the matrice vector product of the linear operator has the expected shape"""
    assert (diffusion * np.ones((np.size(msh.x) * np.size(msh.y),))).shape == (np.size(msh.x) * np.size(msh.y),)


@then("the result of the matrice vector product of the linear operator has the expected values")
def the_result_of_the_matrice_vector_product_of_the_linear_operator_has_the_expected_values(msh, diffusion):
    """the result of the matrice vector product of the linear operator has the expected values"""
    # changer pour un cas non nul
    c = np.array([[1, 2], [3, 4], [5, 6]]).reshape((np.size(msh.x) * np.size(msh.y),))
    truth = np.array([[30, 10], [10, -10], [-10, -30]]).reshape((np.size(msh.x) * np.size(msh.y),))
    # c = np.ones((np.size(msh.x) * np.size(msh.y),))
    # truth = np.array([[0, 0], [0, 0], [0, 0]]).reshape((np.size(msh.x) * np.size(msh.y),))
    assert (diffusion * c == truth).all()


@then("the linear operator is updated as expected at a given time")
def the_linear_operator_is_updated_as_expected_at_a_given_time(diffusion):
    """the linear operator is updated as expected at a given time"""
    diffusion.at_current_time(1.0)
    truth_vert = np.ones((3, 3, 2, 2))
    truth_vert[:, :, 0, 0] = 10  # 5.5
    truth_vert[:, :, 1, 1] = 10  # 5.5
    truth_vert[:, :, 0, 1] = 0  # -4.5
    truth_vert[:, :, 1, 0] = 0  # -4.5
    assert np.max(np.abs(diffusion.K.at_vertical_interface - truth_vert)) < 1e-15
    truth_hori = np.ones((4, 2, 2, 2))
    truth_hori[:, :, 0, 0] = 10  # 5.5
    truth_hori[:, :, 1, 1] = 10  # 5.5
    truth_hori[:, :, 0, 1] = 0  # -4.5
    truth_hori[:, :, 1, 0] = 0  # -4.5
    assert np.max(np.abs(diffusion.K.at_horizontal_interface - truth_hori)) < 1e-15


@then("the update at a given time of the steady linear operator does not change the values")
def the_update_at_a_given_time_of_the_steady_linear_operator_does_not_change_the_values(diffusion_steady):
    """the update at a given time of the steady linear operator does not change the values"""
    diffusion_steady_K_vert = np.copy(diffusion_steady.K.at_vertical_interface)
    diffusion_steady_K_hori = np.copy(diffusion_steady.K.at_horizontal_interface)
    diffusion_steady.at_current_time(1.5)
    assert (diffusion_steady_K_hori == diffusion_steady.K.at_horizontal_interface).all()
    assert (diffusion_steady_K_vert == diffusion_steady.K.at_vertical_interface).all()
