from pathlib import Path

import numpy as np
import pytest
from pytest_bdd import given
from pytest_bdd import scenario
from pytest_bdd import then
from pytest_bdd import when

from source_localization.proximal_gradient import proximal_gradient


@scenario("proximal_gradient.feature", "Test the proximal gradient method")
def test_proximal_gradient():
    """Test the proximal gradient method."""


@given("the differentiable part of a function to minimize and its gradient", target_fixture="f")
def the_differentiable_part_of_a_function_to_minimize_and_its_gradient():
    "the differentiable part of a function to minimize and its gradient"

    def f(X):
        return X[0] ** 2 + X[1] ** 2, np.array([X[0] * 2, X[1] * 2])

    return f


@given("the proximal operator of the other part of the function to minimize", target_fixture="prox_g")
def the_proximal_operator_of_the_other_part_of_the_function_to_minimize():
    "the proximal operator of the other part of the function to minimize"

    def prox_g(X, lamb):
        prox = np.zeros((X.size,))
        for j in range(X.size):
            prox[j] = np.multiply(np.sign(X[j]), np.max([abs(X[j]) - lamb, 0]))
        return prox

    return prox_g


@given("an initial point", target_fixture="X0")
def an_initial_point():
    "an initial point"
    return [0.4, -2]


@given("a step size", target_fixture="step_size")
def a_step_size():
    "a step size"
    return 0.1


@given("a number of iteration", target_fixture="n_ite")
def a_number_of_iteration():
    "a number of iteration"
    return 3


@given("a callback function", target_fixture="callback_fct")
def a_callback_function(tmpdir):
    "a callback function"

    def callback(x):
        global dir_path
        np.save((Path(dir_path) / 'x.npy'), x * 10.0)

    return callback


@when("the proximal gradient algorithm is performed", target_fixture="output")
def the_proximal_gradient_algorithm_is_performed(X0, f, prox_g, step_size, n_ite, tmpdir, callback_fct):
    "the proximal gradient descent algorithm is performed"
    options = {'nit_max': n_ite, 'step size': step_size}
    global dir_path
    dir_path = tmpdir
    xo, fo, dfo, nit = proximal_gradient(X0, f, prox_g, options=options, callback=callback_fct)
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


@then("the outputs of the proximal gradient algorithm have the expected values")
def the_outputs_of_the_proximal_gradient_algorithm_have_the_expected_values(output):
    "the outputs of the proximal gradient algorithm have the expected values"
    x_true = np.array([0.0, -0.78])
    f_true = 0.076**2 + 1.1**2
    df_true = np.array([0.152, -2.2])
    assert np.max(np.abs(output['x'] - x_true)) < 1e-15
    assert np.max(np.abs(output['f'] - f_true)) < 1e-15
    assert np.max(np.abs(output['df'] - df_true)) < 1e-15


@then("the callback function has been executed at each iteration")
def the_callback_function_has_been_executed_at_each_iteration(tmpdir, output):
    "the callback function has been executed at each iteration"
    assert (Path(tmpdir) / 'x.npy').exists()
    x_true = np.array([0.0, -7.8])
    x_saved = np.load((Path(tmpdir) / 'x.npy'))
    assert np.max(np.abs(x_saved - x_true)) < 1e-15


@then("the method fails if the type of algorithm is not implemented")
def the_method_fails_if_the_type_of_algorithm_is_not_implemented(X0, f, prox_g):
    "the method fails if the type of algorithm is not implemented"
    options = {'algorithm': 'not implemented'}
    with pytest.raises(ValueError) as e:
        _, _, _, _ = proximal_gradient(X0, f, prox_g, options=options)
    assert e.type == ValueError
