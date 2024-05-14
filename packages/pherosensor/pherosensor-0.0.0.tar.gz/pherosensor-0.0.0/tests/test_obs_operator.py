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


@scenario("obs_operator.feature", "test the observation operator")
def test_obs_operator():
    """Test the observation operator."""


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


@given("an Obs object", target_fixture='obs')
def an_Obs_object(msh):
    "an Obs object"
    t_obs = np.load(Path("tests/test_data") / "t_obs.npy")
    X_obs = np.load(Path("tests/test_data") / "X_obs.npy")
    d_obs = np.load(Path("tests/test_data") / "d_obs.npy")
    dt_obs_operator = 2.5 * msh.dt

    return Obs(t_obs, X_obs, d_obs, msh, dt_obs_operator=dt_obs_operator)


@given('an estimate of the state variable of the direct model', target_fixture='c_est')
def an_estimate_of_the_state_variable_of_the_direct_model(obs):
    "an estimate of the state variable of the direct model"
    return np.random.random((obs.N_obs, obs.nb_dt_in_obs_time_window))


@when('estimate the observed variable')
def estimate_the_observed_variable(obs, c_est):
    "estimate the observed variable"
    obs.c_est = c_est
    obs.obs_operator()


@then("the estimation of the observed variable has the expected size")
def the_estimation_of_the_observed_variable_has_the_expected_size(obs):
    "the estimation of the observed variable has the expected size"
    assert obs.d_est.size == obs.N_obs


@then("the estimation of the observed variable has the expected value")
def the_estimation_of_the_observed_variable_has_the_expected_value(obs, c_est):
    "the estimation of the observed variable has the expected value"
    assert (obs.d_est == (c_est[:, 0] + c_est[:, 1] + c_est[:, 2]) * obs.msh.dt).all()


@then('the result of the adjoint of the derivative of the obs operator has the expected value')
def the_result_of_the_adjoint_of_the_derivative_of_the_obs_operator_has_the_expected_value(obs):
    "the result of the adjoint of the derivative of the obs operator has the expected value"
    x = np.random.random((obs.N_obs,))
    res = obs.adjoint_derivative_obs_operator(0.49, x)
    res = res.reshape((obs.msh.y.size, obs.msh.x.size))
    truth = [[0.0, x[3] * obs.msh.dt], [0.0, 0.0], [0.0, x[0] * obs.msh.dt]]
    assert (res == truth).all()


@then('the result of the adjoint of the derivative of the one sensor obs operator has the expected value')
def the_result_of_the_adjoint_of_the_derivative_of_the_one_sensor_obs_operator_has_the_expected_value(obs):
    "the result of the adjoint of the derivative of the one sensor obs operator has the expected value"
    x = np.random.random((obs.N_obs,))
    res = obs.onesensor_adjoint_derivative_obs_operator(0.49, x, 4)
    res = res.reshape((obs.msh.y.size, obs.msh.x.size))
    truth = [[0.0, 0.0], [0.0, 0.0], [0.0, x[0] * obs.msh.dt]]
    assert (res == truth).all()


@then("the estimation of the observed variable fails if the estimation of the state variable is not initialized")
def the_estimation_of_the_observed_variable_fails_if_the_estimation_of_the_state_variable_is_not_initialized(msh):
    """the estimation of the observed variable fails if the estimation of the state variable is not initialized"""
    t_obs = np.load(Path("tests/test_data") / "t_obs.npy")
    X_obs = np.load(Path("tests/test_data") / "X_obs.npy")
    d_obs = np.load(Path("tests/test_data") / "d_obs.npy")
    obs_fail = Obs(t_obs, X_obs, d_obs, msh)
    with pytest.raises(ValueError) as e:
        obs_fail.obs_operator()
    assert e.type == ValueError


@then("the initialization fails if the observation operator integration time window is out of the temporal domain")
def the_initialization_fails_if_the_observation_operator_integration_time_window_is_out_of_the_temporal_domain(msh):
    "the initialization fails if the observation operator integration time window is out of the temporal domain"
    t_obs = np.load(Path("tests/test_data") / "t_obs.npy")
    X_obs = np.load(Path("tests/test_data") / "X_obs.npy")
    d_obs = np.load(Path("tests/test_data") / "d_obs.npy")
    with pytest.raises(ValueError) as e:
        Obs(t_obs, X_obs, d_obs, msh, dt_obs_operator=1.5 * np.min(t_obs))
    assert e.type == ValueError


@then("the initialization fails if the observation operator time window overlapps for two data of a same sensor")
def the_initialization_fails_if_the_observation_operator_time_window_overlapps_for_two_data_of_a_same_sensor(msh):
    "the_initialization_fails_if_the_observation_operator_time_window_overlapps_for_two_data_of_a_same_sensor"
    t_obs = np.load(Path("tests/test_data") / "t_obs.npy")
    X_obs = np.load(Path("tests/test_data") / "X_obs.npy")
    d_obs = np.load(Path("tests/test_data") / "d_obs.npy")
    dt_obs_operator = 2.0 * msh.dt
    t_obs[1] = t_obs[0] + 0.5 * dt_obs_operator
    X_obs[1] = X_obs[0]
    with pytest.raises(ValueError) as e:
        Obs(t_obs, X_obs, d_obs, msh, dt_obs_operator=dt_obs_operator)
    assert e.type == ValueError
