from pathlib import Path

import numpy as np
from pytest_bdd import given
from pytest_bdd import scenario
from pytest_bdd import then
from pytest_bdd import when
from scipy.sparse.linalg import LinearOperator as LinOp

from pheromone_dispersion.advection_operator import Advection
from pheromone_dispersion.geom import MeshRect2D
from pheromone_dispersion.velocity import Velocity


@scenario("advection_term.feature", "Generate the convection term of the convection-diffusion PDE as a linear operator")
def test_generate_convection_term_as_linear_operator():
    """Generate the convection term of the convection-diffusion PDE as a linear operator."""


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


@when("initialize the convection linear operator", target_fixture='advection')
def initialize_the_convection_linear_operator(U, msh):
    """initialize the convection linear operator"""
    return Advection(U, msh)


@then("the convection term is a linear operator")
def the_convection_term_is_a_linear_operator(advection):
    """the convection term is a linear operator"""
    assert issubclass(Advection, LinOp) and isinstance(advection, LinOp)


@then("the result of the matrice vector product of the linear operator has the expected shape")
def the_result_of_the_matrice_vector_product_of_the_linear_operator_has_the_expected_shape(msh, advection):
    """the result of the matrice vector product of the linear operator has the expected shape"""
    assert (advection * np.ones((np.size(msh.x) * np.size(msh.y),))).shape == (np.size(msh.x) * np.size(msh.y),)


@then("the result of the matrice vector product of the linear operator has the expected values")
def the_result_of_the_matrice_vector_product_of_the_linear_operator_has_the_expected_values(msh, advection):
    """the result of the matrice vector product of the linear operator has the expected values"""
    truth = np.array([[2, 1], [1, 0], [1, 0]]).reshape((np.size(msh.x) * np.size(msh.y),))
    assert (advection * np.ones((np.size(msh.x) * np.size(msh.y),)) == truth).all()


@then("the opposite sign velocity field is a Velocity object")
def the_opposite_sign_velocity_field_is_a_Velocity_object(advection):
    """the opposite sign velocity field is a Velocity object"""
    assert isinstance(advection.minus_U, Velocity)


@then("the opposite sign velocity field has the expected value")
def the_opposite_sign_velocity_field_has_the_expected_value(U, advection):
    """the opposite sign velocity field has the expected value"""
    assert (advection.minus_U.at_horizontal_interface == -U.at_horizontal_interface).all()
    assert (advection.minus_U.at_vertical_interface == -U.at_vertical_interface).all()


@then("the result of the matrice vector product of the flux part of the adjoint operator has the expected shape")
def the_result_of_the_matrice_vector_product_of_the_flux_part_of_the_adjoint_operator_has_the_expected_shape(msh, advection):
    """the result of the matrice vector product of the flux part of the adjoint operator has the expected shape"""
    prod = advection.rmatvec(np.ones((np.size(msh.x) * np.size(msh.y),)))
    assert prod.shape == (np.size(msh.x) * np.size(msh.y),)


@then("the result of the matrice vector product of the flux part of the adjoint operator has the expected value")
def the_result_of_the_matrice_vector_product_of_the_flux_part_of_the_adjoint_operator_has_the_expected_values(msh, advection):
    """the result of the matrice vector product of the flux part of the adjoint operator has the expected value"""
    truth = np.array([[0, 1], [0, 1], [1, 2]]).reshape((np.size(msh.x) * np.size(msh.y),))
    prod = advection.rmatvec(np.ones((np.size(msh.x) * np.size(msh.y),)))
    assert (prod == truth).all()


@then("the linear operator is updated as expected at a given time")
def the_linear_operator_is_updated_as_expected_at_a_given_time(advection):
    """the linear operator is updated as expected at a given time"""
    advection.at_current_time(0.5, advection.U)
    assert (advection.U.at_horizontal_interface[:, :, 0] == 1.5).all() and (advection.U.at_horizontal_interface[:, :, 1] == -0.5).all()
    assert (advection.U.at_vertical_interface[:, :, 0] == 1.5).all() and (advection.U.at_vertical_interface[:, :, 1] == -0.5).all()
    advection.at_current_time(0.5, advection.minus_U)
    assert (advection.minus_U.at_horizontal_interface[:, :, 0] == -1.5).all() and (
        advection.minus_U.at_horizontal_interface[:, :, 1] == 0.5
    ).all()
    assert (advection.minus_U.at_vertical_interface[:, :, 0] == -1.5).all() and (
        advection.minus_U.at_vertical_interface[:, :, 1] == 0.5
    ).all()
