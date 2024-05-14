from pathlib import Path

import numpy as np
from pytest_bdd import given
from pytest_bdd import scenario
from pytest_bdd import then
from pytest_bdd import when

from pheromone_dispersion.geom import MeshRect2D
from pheromone_dispersion.velocity import Velocity
from source_localization.population_dynamique import PopulationDynamicModel
from source_localization.population_dynamique import StationnaryPopulationDynamicModel


@scenario("population_dynamic_models.feature", "Generate and compute the population dynamic models")
def Generate_and_compute_the_population_dynamic_models():
    """Generate and compute the population dynamic models."""


@given("a mesh", target_fixture="msh")
def a_mesh():
    "a mesh"
    Lx = np.load(Path("tests/test_data") / "Lx.npy")
    Ly = np.load(Path("tests/test_data") / "Ly.npy")
    dx = np.load(Path("tests/test_data") / "dx.npy") * 0.5
    dy = np.load(Path("tests/test_data") / "dy.npy") * 0.5
    Tfinal = np.load(Path("tests/test_data") / "Tfinal.npy")
    msh = MeshRect2D(Lx, Ly, dx, dy, Tfinal - 1e-15)
    t = np.load(Path("tests/test_data") / "t.npy")
    U_vi = np.load(Path("tests/test_data") / "U_vi.npy")
    U_hi = np.load(Path("tests/test_data") / "U_hi.npy")
    U = Velocity(msh, U_vi, U_hi, t=t)
    msh.calc_dt_explicit_solver(U)
    return msh


@when("generate the population dynamic model", target_fixture="PDM")
def generate_the_population_dynamic_model(msh):
    "the population dynamic model"
    return PopulationDynamicModel(msh)


@when("generate the stationnary population dynamic model", target_fixture="SPDM")
def generate_the_stationnary_population_dynamic_model(msh):
    "the stationnary population dynamic model"
    return StationnaryPopulationDynamicModel(msh)


@then("the estimation of the population dynamic models has the expected shape and values")
def the_estimation_of_the_population_dynamic_models_has_the_expected_shape_and_values(msh, PDM, SPDM):
    "the estimation of the population dynamic models has the expected shape and values"
    x_pdm = np.zeros((msh.t_array.size, msh.x.size, msh.y.size))
    x_spdm = np.zeros((msh.t_array.size, msh.x.size, msh.y.size))
    for it, t in enumerate(msh.t_array):
        x_pdm[it, :, :] = t
        for ix, x in enumerate(msh.x):
            x_spdm[it, :, ix] = t + x
    x_pdm = x_pdm.reshape((msh.y.size * msh.x.size * msh.t_array.size,))
    x_spdm = x_spdm.reshape((msh.y.size * msh.x.size * msh.t_array.size,))
    PDM_est = PDM.matvec(x_pdm)
    PDM_est_true = np.ones(((msh.t_array.size - 1) * (msh.x.size - 2) * (msh.y.size - 2)))
    SPDM_est = SPDM.matvec(x_spdm)
    SPDM_est_true = 2 * np.ones(((msh.t_array.size - 1) * msh.x.size * msh.y.size))
    assert PDM_est.shape == ((msh.t_array.size - 1) * msh.x.size * msh.y.size,)
    assert (PDM_est == PDM_est_true).all()
    assert SPDM_est.shape == ((msh.t_array.size - 1) * (msh.x.size - 2) * (msh.y.size - 2),)
    assert (SPDM_est == SPDM_est_true).all()


@then("the estimation of the adjoint of the population dynamic models has the expected shape and values")
def the_estimation_of_the_adjoint_of_the_population_dynamic_models_has_the_expected_shape_and_values(msh, PDM, SPDM):
    "the estimation of the adjoint of the population dynamic models has the expected shape and values"

    v2 = np.random.normal(0, 1, size=msh.y.size * msh.x.size * msh.t_array.size)
    v1 = np.random.normal(0, 1, size=(msh.y.size - 2) * (msh.x.size - 2) * (msh.t_array.size - 1))
    p0 = SPDM.rmatvec(v1)
    p1 = np.dot(v1, SPDM.matvec(v2))
    p2 = np.dot(p0, v2)
    assert np.abs(p1 - p2) < 1e-10
    assert p0.shape == (msh.y.size * msh.x.size * msh.t_array.size,)

    v2 = np.random.normal(0, 1, size=msh.y.size * msh.x.size * msh.t_array.size)
    v1 = np.random.normal(0, 1, size=(msh.y.size) * (msh.x.size) * (msh.t_array.size - 1))
    p0 = PDM.rmatvec(v1)
    p1 = np.dot(v1, PDM.matvec(v2))
    p2 = np.dot(p0, v2)
    assert np.abs(p1 - p2) < 1e-10
    assert p0.shape == (msh.y.size * msh.x.size * msh.t_array.size,)
