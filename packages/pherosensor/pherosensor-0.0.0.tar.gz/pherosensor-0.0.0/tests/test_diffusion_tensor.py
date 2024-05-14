from pathlib import Path

import numpy as np
import pytest
from pytest_bdd import given
from pytest_bdd import scenario
from pytest_bdd import then
from pytest_bdd import when

from pheromone_dispersion.diffusion_tensor import DiffusionTensor
from pheromone_dispersion.geom import MeshRect2D
from pheromone_dispersion.velocity import Velocity


@scenario("diffusion_tensor.feature", "Generate the diffusion tensor")
def test_generate_diffusion_tensor():
    """Generate the diffusion tensor."""


@given("a rectangular 2D mesh", target_fixture="msh")
def a_rectangular_2D_mesh():
    "a rectangular 2D mesh"
    Lx = np.load(Path("tests/test_data") / "Lx.npy")
    Ly = np.load(Path("tests/test_data") / "Ly.npy")
    dx = np.load(Path("tests/test_data") / "dx.npy")
    dy = np.load(Path("tests/test_data") / "dy.npy")
    Tfinal = np.load(Path("tests/test_data") / "Tfinal.npy")
    return MeshRect2D(Lx, Ly, dx, dy, Tfinal)


@given("a velocity field", target_fixture="U")
def a_velocity_field(msh):
    "a velocity field"
    t = np.load(Path("tests/test_data") / "t.npy")
    U_vi = np.load(Path("tests/test_data") / "U_vi.npy")
    U_hi = np.load(Path("tests/test_data") / "U_hi.npy")
    return Velocity(msh, U_vi, U_hi, t=t)


@given("a steady velocity field", target_fixture="U_steady")
def a_steady_velocity_field(msh):
    "a steady velocity field"
    U_vi = np.load(Path("tests/test_data") / "U_vi.npy")
    U_hi = np.load(Path("tests/test_data") / "U_hi.npy")
    return Velocity(msh, U_vi[0, :, :, :], U_hi[0, :, :, :])


@given("a diffusion tensor in the wind direction", target_fixture='K_u')
def a_diffusion_tensor_in_the_wind_direction():
    "a diffusion tensor in the wind direction"
    return np.load(Path("tests/test_data") / "K_u.npy")


@given("a diffusion tensor in the crosswind direction", target_fixture='K_u_t')
def a_diffusion_tensor_in_the_crosswind_direction():
    "a diffusion tensor in the crosswind direction"
    return np.load(Path("tests/test_data") / "K_u_t.npy")


@when("initialize the anisotrope diffusion tensor", target_fixture='K')
def initialize_the_anisotrope_diffusion_tensor(U, K_u, K_u_t):
    """initialize the anisotrope diffusion tensor"""
    return DiffusionTensor(U, K_u, K_u_t)


@when("initialize the steady anisotrope diffusion tensor", target_fixture='K_steady')
def initialize_the_steady_anisotrope_diffusion_tensor(U_steady, K_u, K_u_t):
    """initialize the steady anisotrope diffusion tensor"""
    return DiffusionTensor(U_steady, K_u, K_u_t)


@then("the diffusion tensor at the vertical interfaces has the expected shape")
def the_diffusion_tensor_at_the_vertical_interfaces_has_the_expected_shape(K, U):
    """the diffusion tensor at the vertical interfaces has the expected shape"""
    assert K.at_vertical_interface.shape == (U.at_vertical_interface.shape[0], U.at_vertical_interface.shape[1], 2, 2)


@then("the expected diffusion tensor at the vertical interfaces is computed")
def the_expected_diffusion_tensor_at_the_vertical_interfaces_is_computed(K):
    """the expected diffusion tensor at the vertical interfaces is computed"""
    truth = np.ones((3, 3, 2, 2))
    truth[:, :, 0, 0] = 5.5
    truth[:, :, 1, 1] = 5.5
    truth[:, :, 0, 1] = 4.5
    truth[:, :, 1, 0] = 4.5
    assert np.max(np.abs(K.at_vertical_interface - truth)) < 1e-15


@then("the diffusion tensor at the horizontal interfaces has the expected shape")
def the_diffusion_tensor_at_the_horizontal_interfaces_has_the_expected_shape(K, U):
    """the diffusion tensor at the horizontal interfaces has the expected shape"""
    assert K.at_horizontal_interface.shape == (U.at_horizontal_interface.shape[0], U.at_horizontal_interface.shape[1], 2, 2)


@then("the expected diffusion tensor at the horizontal interfaces is computed")
def the_expected_diffusion_tensor_at_the_horizontal_interfaces_is_computed(K):
    """the expected diffusion tensor at the horizontal interfaces is computed"""
    truth = np.ones((4, 2, 2, 2))
    truth[:, :, 0, 0] = 5.5
    truth[:, :, 1, 1] = 5.5
    truth[:, :, 0, 1] = 4.5
    truth[:, :, 1, 0] = 4.5
    assert np.max(np.abs(K.at_horizontal_interface - truth)) < 1e-15


@then("the expected diffusion tensor at a given time is computed")
def the_expected_diffusion_tensor_at_a_given_time_is_computed(K):
    """the expected diffusion tensor at a given time is computed"""
    K.at_current_time(1.0)
    truth_vert = np.ones((3, 3, 2, 2))
    truth_vert[:, :, 0, 0] = 5.5
    truth_vert[:, :, 1, 1] = 5.5
    truth_vert[:, :, 0, 1] = -4.5
    truth_vert[:, :, 1, 0] = -4.5
    assert np.max(np.abs(K.at_vertical_interface - truth_vert)) < 1e-15
    truth_hori = np.ones((4, 2, 2, 2))
    truth_hori[:, :, 0, 0] = 5.5
    truth_hori[:, :, 1, 1] = 5.5
    truth_hori[:, :, 0, 1] = -4.5
    truth_hori[:, :, 1, 0] = -4.5
    assert np.max(np.abs(K.at_horizontal_interface - truth_hori)) < 1e-15


@then("the update fails if the time is not between the lowest and largest times contained in the time vector")
def the_update_fails_if_the_time_is_not_between_the_lowest_and_largest_times_contained_in_the_time_vector(K):
    """the update fails if the time is not between the lowest and largest times contained in the time vector"""
    with pytest.raises(ValueError) as e:
        K.at_current_time(max(K.U.t) + 1)
    assert e.type == ValueError


@then("the update at a given time of the steady diffusion tensor does not change the values")
def the_update_at_a_given_time_of_the_steady_diffusion_tensor_does_not_change_the_values(K_steady):
    """the update at a given time of the steady diffusion tensor does not change the values"""
    K_steady_Hori_save = np.copy(K_steady.at_horizontal_interface)
    K_steady_Vert_save = np.copy(K_steady.at_vertical_interface)
    K_steady.at_current_time(1.5)
    assert (K_steady_Hori_save == K_steady.at_horizontal_interface).all()
    assert (K_steady_Vert_save == K_steady.at_vertical_interface).all()
