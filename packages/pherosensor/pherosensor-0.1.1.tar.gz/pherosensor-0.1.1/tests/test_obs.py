from pathlib import Path

import numpy as np
import pytest
from pytest_bdd import given
from pytest_bdd import scenario
from pytest_bdd import then
from pytest_bdd import when

from pheromone_dispersion.geom import MeshRect2D
from pheromone_dispersion.velocity import Velocity
from source_localization.obs import Obs


@scenario("obs.feature", "Generate the obs object")
def test_generate_obs():
    """Generate the Obs object."""


@given("a rectangular 2D mesh", target_fixture="msh")
def a_rectangular_2D_mesh():
    "a rectangular 2D mesh"
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


@given("the observations time", target_fixture="t_obs")
def the_observations_time():
    "the observations time"
    return np.load(Path("tests/test_data") / "t_obs.npy")


@given("the observations location", target_fixture="X_obs")
def the_observations_location():
    "the observations location"
    return np.load(Path("tests/test_data") / "X_obs.npy")


@given("the observations", target_fixture="d_obs")
def the_observations():
    "the observations"
    return np.load(Path("tests/test_data") / "d_obs.npy")


@when("generate the Obs object", target_fixture='obs')
def genreate_the_Obs_object(t_obs, X_obs, d_obs, msh):
    "generate the Obs object"
    dt_obs_operator = 2.5 * msh.dt
    return Obs(t_obs, X_obs, d_obs, msh, dt_obs_operator=dt_obs_operator)


@then("the vector of the position of the sensors has the expected shape and value")
def the_vector_of_the_position_of_the_sensors_has_the_expected_shape_and_value(obs):
    "the vector of the position of the sensors has the expected shape and value"
    assert obs.X_sensors.shape == (5, 2)
    for X_obs in obs.X_obs:
        assert X_obs in obs.X_sensors


@then("the number of sensors has the expected value")
def the_number_of_sensors_has_the_expected__value(obs):
    "the number of sensors has the expected value"
    assert obs.nb_sensors == 5


@then("the number of time step over which the data are integrated has the expected value")
def the_number_of_time_step_over_which_the_data_are_integrated_has_the_expected_value(obs):
    "the number of time step over which the data are integrated has the expected value"
    assert obs.nb_dt_in_obs_time_window == 3


@then("the vector of the index of the time of estimation has the expected shape and value")
def the_vector_of_the_index_of_the_time_of_estimation_has_the_expected_shape_and_value(obs):
    "the vector of the index of the time of estimation has the expected shape and value"
    truth = [[5, 4, 3], [4, 3, 2], [9, 8, 7], [7, 6, 5], [10, 9, 8]]
    assert obs.index_obs_to_index_time_est.shape == (5, 3)
    assert (obs.index_obs_to_index_time_est == truth).all()


@then("the dictionnary containing the indexes of the observations given an estimation time has the expected values")
def the_dictionnary_containing_the_indexes_of_the_observations_given_an_estimation_time_has_the_expected_values(obs):
    "the dictionnary containing the indexes of the observations given an estimation time has the expected values"
    assert obs.index_time_est_to_index_obs[2] == [1]
    assert obs.index_time_est_to_index_obs[3] == [1, 0]
    assert obs.index_time_est_to_index_obs[4] == [1, 0]
    assert obs.index_time_est_to_index_obs[5] == [0, 3]
    assert obs.index_time_est_to_index_obs[6] == [3]
    assert obs.index_time_est_to_index_obs[7] == [3, 2]
    assert obs.index_time_est_to_index_obs[8] == [2, 4]
    assert obs.index_time_est_to_index_obs[9] == [2, 4]
    assert obs.index_time_est_to_index_obs[10] == [4]


@then("the initialization fails if the observations array has more than one dimension")
def the_initialization_fails_if_the_observations_array_has_more_than_one_dimension(t_obs, X_obs, d_obs, msh):
    "the initialization fails if the observations array has more than one dimension"
    with pytest.raises(ValueError) as e:
        Obs(t_obs, X_obs, np.array([d_obs, d_obs]), msh)
    assert e.type == ValueError


@then("the initialization fails if the observations time array does not have the expected size")
def the_initialization_fails_if_the_observations_time_array_does_not_have_the_expected_size(t_obs, X_obs, d_obs, msh):
    "the initialization fails if the observations time array does not have the expected size"
    with pytest.raises(ValueError) as e:
        Obs(t_obs[:-2], X_obs, d_obs, msh)
    assert e.type == ValueError


@then("the initialization fails if the observations location array does not have the expected size")
def the_initialization_fails_if_the_observations_location_array_does_not_have_the_expected_size(t_obs, X_obs, d_obs, msh):
    "the initialization fails if the observations location array does not have the expected size"
    with pytest.raises(ValueError) as e:
        Obs(t_obs, X_obs[:-2], d_obs, msh)
    assert e.type == ValueError


@then("the initialization fails if the time array is not initialized")
def the_initialization_fails_if_the_time_array_is_not_initialized(t_obs, X_obs, d_obs):
    "the initialization fails if the time array is not initialized"
    Lx = np.load(Path("tests/test_data") / "Lx.npy")
    Ly = np.load(Path("tests/test_data") / "Ly.npy")
    dx = np.load(Path("tests/test_data") / "dx.npy")
    dy = np.load(Path("tests/test_data") / "dy.npy")
    Tfinal = np.load(Path("tests/test_data") / "Tfinal.npy")
    msh = MeshRect2D(Lx, Ly, dx, dy, Tfinal - 1e-15)
    with pytest.raises(ValueError) as e:
        Obs(t_obs, X_obs, d_obs, msh)
    assert e.type == ValueError


@then("the initialization fails if one of the observations is out of the spatial domain")
def the_initialization_fails_if_one_of_the_observations_is_out_of_the_spatial_domain(msh, t_obs, X_obs, d_obs):
    "the initialization fails if one of the observations is out of the spatial domain"
    X_obs[0, 0] = np.min(msh.x_vertical_interface) - 1.0
    with pytest.raises(ValueError) as e:
        Obs(t_obs, X_obs, d_obs, msh)
    assert e.type == ValueError
    X_obs[0, 0] = np.max(msh.x_vertical_interface) + 1.0
    with pytest.raises(ValueError) as e:
        Obs(t_obs, X_obs, d_obs, msh)
    assert e.type == ValueError
    X_obs[0, 0] = 0.5 * (np.min(msh.x) + np.max(msh.x))
    X_obs[0, 1] = np.min(msh.y_horizontal_interface) - 1.0
    with pytest.raises(ValueError) as e:
        Obs(t_obs, X_obs, d_obs, msh)
    assert e.type == ValueError
    X_obs[0, 1] = np.max(msh.y_horizontal_interface) + 1.0
    with pytest.raises(ValueError) as e:
        Obs(t_obs, X_obs, d_obs, msh)
    assert e.type == ValueError


@then("the initialization fails if one of the observations is out of the temporal domain")
def the_initialization_fails_if_one_of_the_observations_is_out_of_the_temporal_domain(msh, t_obs, X_obs, d_obs):
    "the initialization fails if one of the observations is out of the temporal domain"
    t_obs[0] = np.min(msh.t_array) - 1
    with pytest.raises(ValueError) as e:
        Obs(t_obs, X_obs, d_obs, msh)
    assert e.type == ValueError
    t_obs[0] = np.max(msh.t_array) + 1
    with pytest.raises(ValueError) as e:
        Obs(t_obs, X_obs, d_obs, msh)
    assert e.type == ValueError
