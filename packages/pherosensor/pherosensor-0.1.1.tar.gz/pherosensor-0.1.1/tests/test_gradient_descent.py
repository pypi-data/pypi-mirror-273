from pathlib import Path

import numpy as np
import pytest
from pytest_bdd import given
from pytest_bdd import scenario
from pytest_bdd import then
from pytest_bdd import when

from source_localization.gradient_descent import gradient_descent


@scenario("gradient_descent.feature", "Test the gradient descent method")
def test_gradient_descent():
    """Test the gradient descent method."""


@given("a function to minimize and its gradient", target_fixture="f")
def a_function_to_minimize_and_its_gradient():
    "a function to minimize and its gradient"

    def f(X):
        return X[0] ** 2 + X[1] ** 2, np.array([X[0] * 2, X[1] * 2])

    return f


@given("an initial point", target_fixture="X0")
def an_initial_point():
    "an initial point"
    return [-10, 20]


@given("a step size", target_fixture="step_size")
def a_step_size():
    "a step size"
    return 0.75


@given("a too big step size", target_fixture="big_step_size")
def a_too_big_step_size():
    "a too big step size"
    return 1.75


@given("a number of iteration", target_fixture="n_ite")
def a_number_of_iteration():
    "a number of iteration"
    return 3


@given("a callback function", target_fixture="callback_fct")
def a_callback_function(tmpdir):
    "a callback function"

    def callback(x):
        global dir_path
        np.save((Path(dir_path) / 'x.npy'), x / 5.0)

    return callback


@when("the gradient descent algorithm is performed", target_fixture="output")
def the_gradient_descent_algorithm_is_performed(X0, f, step_size, n_ite, tmpdir, callback_fct):
    "the gradient descent algorithm is performed"
    options = {'nit_max': n_ite, 'step size': step_size}
    global dir_path
    dir_path = tmpdir
    xo, fo, dfo, nit = gradient_descent(f, X0, options=options, callback=callback_fct)
    output = {}
    output['x'] = xo
    output['f'] = fo
    output['df'] = dfo
    output['nb iter'] = nit
    return output


@then("the termination criteria is reached")
def the_termination_criteria_is_reached(n_ite, output):
    "the termination criteria is reached"
    assert output['nb iter'] == n_ite


@then("the outputs of the gradient descent algorithm have the expected values")
def the_outputs_of_the_gradient_descent_algorithm_have_the_expected_values(output):
    "the outputs of the gradient descent algorithm have the expected values"
    x_true = np.array([1.25, -2.5])
    f_true = 2.5**2 + 5**2
    df_true = np.array([-5, 10])
    assert (output['x'] == x_true).all()
    assert output['f'] == f_true
    assert (output['df'] == df_true).all()


@then("the callback function has been executed at each iteration")
def the_callback_function_has_been_executed_at_each_iteration(tmpdir, output):
    "the callback function has been executed at each iteration"
    assert (Path(tmpdir) / 'x.npy').exists()
    x_true = np.array([0.25, -0.5])
    x_saved = np.load((Path(tmpdir) / 'x.npy'))
    assert (x_true == x_saved).all()


@then("the algorithm fails if function does not decreases")
def the_algorithm_fails_if_function_does_not_decreases(X0, f, big_step_size):
    "the algorithm fails if function does not decreases"
    options = {'step size': big_step_size}
    with pytest.raises(ValueError) as e:
        _, _, _, _ = gradient_descent(f, X0, options=options)
    assert e.type == ValueError
