from pathlib import Path

import numpy as np
from pytest_bdd import given
from pytest_bdd import scenario
from pytest_bdd import then
from pytest_bdd import when

from pheromone_dispersion.gaussian_plume import Gaussian_plume_1source
from pheromone_dispersion.gaussian_plume import Gaussian_plume_multisources
from pheromone_dispersion.geom import MeshRect2D


@scenario("gaussian_plume.feature", "Generate and compute the Gaussian plume")
def test_generate_and_compute_gaussian_plume():
    """Generate and compute the Gaussian plume."""


@given("a rectangular 2D mesh", target_fixture="msh")
def a_rectangular_2D_mesh():
    "a rectangular 2D mesh"
    Lx = np.load(Path("tests/test_data") / "Lx.npy")
    Ly = np.load(Path("tests/test_data") / "Ly.npy")
    dx = np.load(Path("tests/test_data") / "dx.npy")
    dy = np.load(Path("tests/test_data") / "dy.npy")
    Tfinal = np.load(Path("tests/test_data") / "Tfinal.npy")
    return MeshRect2D(Lx, Ly, dx, dy, Tfinal)


@given("a source location", target_fixture="Xs")
def a_source_location():
    "a source location"
    return [-1, -1, 1]  # np.load(Path("tests/test_data")/"Xs.npy")


@given("an emission rate of the source", target_fixture="Q")
def an_emission_rate_of_the_source():
    "an emission rate of the source"
    return 1  # np.load(Path("tests/test_data")/"Q.npy")


@given("a constant diffusion coefficient", target_fixture="K")
def a_constant_diffusion_coefficient():
    "a constant diffusion coefficient"
    return 1  # np.load(Path("tests/test_data")/"Q.npy")


@given("a constant wind velocity", target_fixture="u")
def a_constant_wind_velocity():
    "a constant wind velocity"
    return 1  # np.load(Path("tests/test_data")/"Q.npy")


@given("a settling velocity", target_fixture="w_set")
def a_settling_velocity():
    "asettling velocity"
    return 0  # np.load(Path("tests/test_data")/"Q.npy")


@given("a deposition velocity", target_fixture="w_dep")
def a_deposition_velocity():
    "a deposition velocity"
    return 0  # np.load(Path("tests/test_data")/"Q.npy")


@when("initialize the single source gaussian plume", target_fixture='gp_1src')
def initialize_the_single_source_gaussian_plume(Xs, K, u, Q, w_set, w_dep):
    """initialize the single source gaussian plume"""
    return Gaussian_plume_1source(Xs, K, u, Q, w_set, w_dep)


@when("initialize the multiple sources gaussian plume", target_fixture='gp_multisrc')
def initialize_the_multiple_sources_gaussian_plume(Xs, K, u, Q, w_set, w_dep):
    """initialize the multiple sources gaussian plume"""
    return Gaussian_plume_multisources([Xs], K, u, [Q], w_set, w_dep)


@then("the change of variable has the expected shape")
def the_change_of_variable_has_the_expected_shape(msh, gp_1src):
    """the change of variable has the expected shape"""
    assert gp_1src.CDV(msh.x).shape == msh.x.shape


@then("the change of variable has the expected value")
def the_change_of_variable_has_the_expected_value(msh, gp_1src):
    """the change of variable has the expected value"""
    assert (gp_1src.CDV(msh.x) == msh.x).all()


@then("the single source gaussian plume has the expected shape")
def the_single_source_gaussian_plume_has_the_expected_shape(msh, gp_1src):
    """the single source gaussian plume has the expected shape"""
    xv, yv, zv = np.meshgrid(msh.x, msh.y, np.array([0, 1]), sparse=True, indexing='ij')
    assert gp_1src.gaussian_plume(xv, yv, zv).shape == (msh.x.size, msh.y.size, 2)


@then("the single source gaussian plume has the expected value")
def the_single_source_gaussian_plume_has_the_expected_value(msh, Xs, K, u, Q, gp_1src):
    """the single source gaussian plume has the expected value"""
    xv, yv = np.meshgrid(msh.x, msh.y, sparse=True, indexing='ij')
    truth = np.array(
        [
            [np.exp(-13.0 / 24.0) / 3.0 / np.pi, np.exp(-29.0 / 24.0) / 3.0 / np.pi, np.exp(-53.0 / 24.0) / 3.0 / np.pi],
            [np.exp(-13.0 / 40.0) / 5.0 / np.pi, np.exp(-29.0 / 40.0) / 5.0 / np.pi, np.exp(-53.0 / 40.0) / 5.0 / np.pi],
        ]
    )
    assert gp_1src.gaussian_plume(Xs[0] + 0.25 * u * Xs[2] ** 2 / K, -1, 0) == 2 * Q / (np.pi * u * Xs[2] ** 2 * np.exp(1))
    assert (np.abs(gp_1src.gaussian_plume(xv, yv, 0) - truth) < 1e-16).all()
    assert (gp_1src.gaussian_plume(0.25 * u * Xs[2] ** 2 / K, -1, 0) > gp_1src.gaussian_plume(msh.x, -1, 0)).all()


@then("the multiple sources gaussian plume has the expected shape")
def the_multiple_sources_gaussian_plume_has_the_expected_shape(msh, gp_multisrc):
    """the multiple sources gaussian plume has the expected shape"""
    xv, yv, zv = np.meshgrid(msh.x, msh.y, np.array([0, 1]), sparse=True, indexing='ij')
    assert gp_multisrc.gaussian_plume(xv, yv, zv).shape == (msh.x.size, msh.y.size, 2)


@then("the multiple sources gaussian plume has the expected value with one source")
def the_multiple_sources_gaussian_plume_has_the_expected_value_with_one_source(msh, Xs, K, u, Q, gp_multisrc):
    """the multiple sources gaussian plume has the expected value with one source"""
    xv, yv = np.meshgrid(msh.x, msh.y, sparse=True, indexing='ij')
    truth = np.array(
        [
            [np.exp(-13.0 / 24.0) / 3.0 / np.pi, np.exp(-29.0 / 24.0) / 3.0 / np.pi, np.exp(-53.0 / 24.0) / 3.0 / np.pi],
            [np.exp(-13.0 / 40.0) / 5.0 / np.pi, np.exp(-29.0 / 40.0) / 5.0 / np.pi, np.exp(-53.0 / 40.0) / 5.0 / np.pi],
        ]
    )
    assert gp_multisrc.gaussian_plume(Xs[0] + 0.25 * u * Xs[2] ** 2 / K, -1, 0) == 2 * Q / (np.pi * u * Xs[2] ** 2 * np.exp(1))
    assert (np.abs(gp_multisrc.gaussian_plume(xv, yv, 0) - truth) < 1e-16).all()
    assert (gp_multisrc.gaussian_plume(0.25 * u * Xs[2] ** 2 / K, 0, 0) > gp_multisrc.gaussian_plume(msh.x, 0, 0)).all()
