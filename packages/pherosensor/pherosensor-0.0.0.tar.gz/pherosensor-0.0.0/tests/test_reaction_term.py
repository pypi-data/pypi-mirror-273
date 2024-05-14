from pathlib import Path

import numpy as np
import pytest
from pytest_bdd import given
from pytest_bdd import scenario
from pytest_bdd import then
from pytest_bdd import when
from scipy.sparse.linalg import LinearOperator as LinOp

from pheromone_dispersion.geom import MeshRect2D
from pheromone_dispersion.reaction_operator import Reaction

"""
Tester que les valeurs des attributs sont bon et de bonnes dimensions, que les operateurs
lineaires ont bien le bon type et la bonne dimension quand appliquee, que la res de l'EDP
soit bonne et de bonne dimension
"""


@scenario("reaction_term.feature", "Generate the reaction term of the convection-diffusion PDE as a linear operator")
def test_generate_reaction_term_as_linear_operator():
    """Generate the reaction term of the convection-diffusion PDE as a linear operator."""


@given("a deposition coefficient", target_fixture="depot_coeff")
def a_deposition_coefficient():
    "a deposition coefficient"
    depot_coeff = np.load(Path("tests/test_data") / "depot_coeff.npy")
    return depot_coeff


@given("an invalid deposition coefficient", target_fixture="depot_coeff_invalid")
def an_invalid_deposition_coefficient():
    "an invalid deposition coefficient"
    depot_coeff = np.load(Path("tests/test_data") / "depot_coeff_invalid.npy")
    return depot_coeff


@given("a rectangular 2D mesh", target_fixture="msh")
def a_rectangular_2D_mesh():
    "a rectangular 2D mesh"
    Lx = np.load(Path("tests/test_data") / "Lx.npy")
    Ly = np.load(Path("tests/test_data") / "Ly.npy")
    dx = np.load(Path("tests/test_data") / "dx.npy")
    dy = np.load(Path("tests/test_data") / "dy.npy")
    Tfinal = np.load(Path("tests/test_data") / "Tfinal.npy")
    return MeshRect2D(Lx, Ly, dx, dy, Tfinal)


@when("initialize the reaction linear operator", target_fixture='reaction')
def initialize_the_reaction_linear_operator(depot_coeff, msh):
    """initialize the reaction linear operator"""
    return Reaction(depot_coeff, msh)


@then("the reaction term is a linear operator")
def the_reaction_term_is_a_linear_operator(reaction):
    """the reaction term is a linear operator"""
    assert issubclass(Reaction, LinOp) and isinstance(reaction, LinOp)


@then("the result of the matrice vector product of the linear operator has the expected shape")
def the_result_of_the_matrice_vector_product_of_the_linear_operator_has_the_expected_shape(depot_coeff, reaction):
    """the result of the matrice vector product of the linear operator has the expected shape"""
    assert (reaction * np.ones((np.size(depot_coeff),))).shape == (np.size(depot_coeff),)


@then("the result of the matrice vector product of the linear operator has the expected values")
def the_result_of_the_matrice_vector_product_of_the_linear_operator_has_the_expected_values(depot_coeff, reaction):
    """the result of the matrice vector product of the linear operator has the expected values"""
    truth = np.array(depot_coeff).reshape((np.size(depot_coeff),))
    assert (reaction * np.ones((np.size(depot_coeff),)) == truth).all()


@then("the reaction coefficient is correctly updated")
def the_reaction_coefficient_is_correctly_updated(depot_coeff, reaction):
    """the reaction coefficient is correctly updated"""
    new_coeff = np.random.random(depot_coeff.shape)
    reaction.update_reaction_coeff(new_coeff)
    assert (reaction.reaction_coeff == new_coeff).all()
    assert (reaction * np.ones((np.size(depot_coeff),)) == new_coeff.reshape((np.size(depot_coeff),))).all()


@then("the initialization fails if the deposition coefficient shape does not match the shape of the mesh")
def the_initialization_fails_if_the_deposition_coefficient_shape_does_not_match_the_shape_of_the_mesh(depot_coeff_invalid, msh):
    """the initialization fails if the deposition coefficient shape does not match the shape of the mesh"""
    with pytest.raises(ValueError) as e:
        Reaction(depot_coeff_invalid, msh)
    assert e.type == ValueError
