import numpy as np
from scipy.sparse.linalg import LinearOperator as LinOp

from pheromone_dispersion.velocity import Velocity


def sum_advection_flux_given_U(U, x, msh):
    """
    compute the sum over a cell of the flux of the advection term for a given velocity field

    - TO BE DONE:
        * change the BC, for now: no income, change for: a given income
    - input:
        * U: object of the class Velocity
        * x:
            numpy array of shape (msh.x.size, msh.y.size), contains the concentration of pheromones
        * msh: object of the class MeshRect2D
    - output:
        * sum_faces: the sum over a cell of the flux
    """

    shift_vertical = np.zeros((msh.y_horizontal_interface.size, msh.x.size))
    flux_vertical = np.zeros((msh.y_horizontal_interface.size, msh.x.size))

    # Computation of the y-component of the flux
    shift_vertical[:-1, :] = x[:, :]  # temporary value on the boundary : boundary conditions are dealt with later
    flux_vertical[U.cell_above_upwind] = U.at_horizontal_interface[:, :, 1][U.cell_above_upwind] * shift_vertical[U.cell_above_upwind]
    shift_vertical[1:, :] = x[:, :]
    shift_vertical[0, :] = 0  # temporary value on the boundary : boundary conditions are dealt with later
    flux_vertical[U.cell_under_upwind] += U.at_horizontal_interface[:, :, 1][U.cell_under_upwind] * shift_vertical[U.cell_under_upwind]

    # Boundary Condition on the y-component of the flux
    flux_vertical[-1, U.cell_above_upwind[-1, :]] = 0
    flux_vertical[0, U.cell_under_upwind[0, :]] = 0

    shift_horizontal = np.zeros((msh.y.size, msh.x_vertical_interface.size))
    flux_horizontal = np.zeros((msh.y.size, msh.x_vertical_interface.size))

    # Computation of the x-component of the flux
    shift_horizontal[:, :-1] = x[:, :]  # temporary value on the boundary : boundary conditions are dealt with later
    flux_horizontal[U.cell_right_upwind] = (
        U.at_vertical_interface[:, :, 0][U.cell_right_upwind] * shift_horizontal[U.cell_right_upwind]
    )  # transport
    shift_horizontal[:, 1:] = x[:, :]
    shift_horizontal[:, 0] = 0  # temporary value on the boundary : boundary conditions are dealt with later
    flux_horizontal[U.cell_left_upwind] += (
        U.at_vertical_interface[:, :, 0][U.cell_left_upwind] * shift_horizontal[U.cell_left_upwind]
    )  # transport

    # Boundary Condition on the x-component of the flux
    flux_horizontal[U.cell_right_upwind[:, -1], -1] = 0
    flux_horizontal[U.cell_left_upwind[:, 0], 0] = 0

    # Computation of the flux over the border of the cell for a cartesian mesh
    sum_faces = (
        msh.dy * (flux_horizontal[:, 1:] - flux_horizontal[:, :-1]) + msh.dx * (flux_vertical[1:, :] - flux_vertical[:-1, :])
    ) / msh.mass_cell
    return sum_faces


class Advection(LinOp):
    """
    Class containing the convection term linear operator of the PDE
    Subclass of the scipy.sparse.linalg.LinearOperator class,
    see https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.LinearOperator.html
    """

    def __init__(self, U, msh):
        """
        Instanciation of the class.

        - input:
            * U: object of the class Velocity
            * msh: object of the class MeshRect2D
        - attributes:
            * U: object of the class Velocity
            * minus_U: object of the class Velocity, the opposite sign velocity field
            * msh: object of the class MeshRect2D
            * shape: tuple of integers, shape of the matrix of the linear operator
            * dtype: data type object, data type of the element of the matrix of the linear operator
        """

        self.U = U
        if U.t is None:
            self.minus_U = Velocity(msh, -U.at_vertical_interface, -U.at_horizontal_interface)
        else:
            minus_U_at_vertical_interface = np.zeros((U.t.size, U.at_vertical_interface.shape[0], U.at_vertical_interface.shape[1], 2))
            minus_U_at_horizontal_interface = np.zeros(
                (U.t.size, U.at_horizontal_interface.shape[0], U.at_horizontal_interface.shape[1], 2)
            )
            for it, tc in enumerate(U.t):
                U.at_current_time(tc)
                minus_U_at_vertical_interface[it, :, :, :] = -U.at_vertical_interface
                minus_U_at_horizontal_interface[it, :, :, :] = -U.at_horizontal_interface
            self.minus_U = Velocity(msh, minus_U_at_vertical_interface, minus_U_at_horizontal_interface, t=U.t)
            U.at_current_time(U.t[0])
        self.msh = msh
        self.shape = (self.msh.y.size * self.msh.x.size, self.msh.y.size * self.msh.x.size)
        self.dtype = np.dtype(float)

    def at_current_time(self, tc, U):
        """
        Update the velocity field U at a given time.

        - input:
            * tc: the current time
            * U: object of the class Velocity, velocity field to be updated
        - do:
            * update the velocity field U and its attribute using the method at_current_time of the class Velocity
        """

        U.at_current_time(tc)

    def _matvec(self, x_out):
        """
        Compute the image (matrix-vector product) of the convection linear operator for a given vector of concentration

        - input:
            * x_out:
                numpy array of shape (msh.x.size*msh.y.size, ),
                contains the concentration of pheromones raveled into a vector to match the format of the LinearOperator class
        - output:
            * numpy array of shape (msh.x.size*msh.y.size, ), the image of the convection linear operator for the given concentration
        """

        # reshape the vector (of (msh.x.size*msh.y.size, )) containg the concentration into a matrix (of shape (msh.y.size, msh.x.size))
        x = x_out.reshape((self.msh.y.size, self.msh.x.size))  # unknown of the PDE

        sum_faces = sum_advection_flux_given_U(self.U, x, self.msh)

        return sum_faces.reshape((self.msh.y.size * self.msh.x.size,))

    def _rmatvec(self, x_out):
        """
        Compute the image (matrix-vector product) of the flux part of the adjoint of the convection linear operator
        for a given vector of concentration.
        This flux part of the adjoint operator is the adjoint operator if the velocity field has a divergence equal to 0

        - input:
            * x_out:
                numpy array of shape (msh.x.size*msh.y.size, ),
                contains the concentration of pheromones raveled into a vector to match the format of the LinearOperator class
        - output:
            * numpy array of shape (msh.x.size*msh.y.size, ), the image of adjoint the convection linear operator for a given concentration
        """

        # reshape the vector (of (msh.x.size*msh.y.size, )) containg the concentration into a matrix (of shape (msh.y.size, msh.x.size))
        x = x_out.reshape((self.msh.y.size, self.msh.x.size))  # unknown of the PDE

        sum_faces = sum_advection_flux_given_U(self.minus_U, x, self.msh)

        return sum_faces.reshape((self.msh.y.size * self.msh.x.size,))

    def _matmat(self, x_out):
        """
        Compute the image (matrix-matrix product) of the advection linear operator for a given (matrix of) concentration

        - input:
            * x_out:
                numpy array of (shape msh.x.size*msh.y.size, msh.x.size*msh.y.size),
                contains the concentration of pheromones raveled into a vector to match the format of the LinearOperator class
        - output:
            * numpy array of shape (msh.x.size*msh.y.size, msh.x.size*msh.y.size),
              the image of the convection linear operator for the given concentration
        """
        return np.hstack([self.matvec(col.reshape(-1, 1)) for col in x_out.T])


class AdvectionAdjoint(LinOp):
    """
    Class containing the adjoint convection term linear operator of the PDE
    This class and it method _matvec are redundant with the _rmatvec function of the class Advection
    but this class is meant for the implicit scheme of the adjoint model
    Subclass of the scipy.sparse.linalg.LinearOperator class,
    see https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.LinearOperator.html
    """

    def __init__(self, U, msh):
        """
        Instanciation of the class.

        - input:
            * U: object of the class Velocity
            * msh: object of the class MeshRect2D
        - attributes:
            * U: object of the class Velocity
            * minus_U: object of the class Velocity, the opposite sign velocity field
            * msh: object of the class MeshRect2D
            * shape: tuple of integers, shape of the matrix of the linear operator
            * dtype: data type object, data type of the element of the matrix of the linear operator
        """

        self.U = U
        if U.t is None:
            self.minus_U = Velocity(msh, -U.at_vertical_interface, -U.at_horizontal_interface)
        else:
            minus_U_at_vertical_interface = np.zeros((U.t.size, U.at_vertical_interface.shape[0], U.at_vertical_interface.shape[1], 2))
            minus_U_at_horizontal_interface = np.zeros(
                (U.t.size, U.at_horizontal_interface.shape[0], U.at_horizontal_interface.shape[1], 2)
            )
            for it, tc in enumerate(U.t):
                U.at_current_time(tc)
                minus_U_at_vertical_interface[it, :, :, :] = -U.at_vertical_interface
                minus_U_at_horizontal_interface[it, :, :, :] = -U.at_horizontal_interface
            self.minus_U = Velocity(msh, minus_U_at_vertical_interface, minus_U_at_horizontal_interface, t=U.t)
            U.at_current_time(U.t[0])
        self.msh = msh
        self.shape = (self.msh.y.size * self.msh.x.size, self.msh.y.size * self.msh.x.size)
        self.dtype = np.dtype(float)

    def at_current_time(self, tc):
        """
        Update the attributes U and minus_U of the class at a given time.

        - input:
            * tc: the current time
        """
        self.U.at_current_time(tc)
        self.minus_U.at_current_time(tc)

    def _matvec(self, x_out):
        """
        Compute the image (matrix-vector product) of the adjoint of the convection linear operator for a given vector of concentration

        - input:
            * x_out:
                numpy array of shape (msh.x.size*msh.y.size, ),
                contains the concentration of pheromones raveled into a vector to match the format of the LinearOperator class
        - output:
            * numpy array of shape (msh.x.size*msh.y.size, ), the image of the convection linear operator for the given concentration
        """

        # reshape the vector (of (msh.x.size*msh.y.size, )) containg the concentration into a matrix (of shape (msh.y.size, msh.x.size))
        x = x_out.reshape((self.msh.y.size, self.msh.x.size))  # unknown of the PDE

        sum_faces = sum_advection_flux_given_U(self.minus_U, x, self.msh) + self.U.div * x

        return sum_faces.reshape((self.msh.y.size * self.msh.x.size,))

    def _matmat(self, x_out):
        """
        Compute the image (matrix-matrix product) of the adjoint advection linear operator for a given (matrix of) concentration

        - input:
            * x_out:
                numpy array of (shape msh.x.size*msh.y.size, msh.x.size*msh.y.size),
                contains the concentration of pheromones raveled into a vector to match the format of the LinearOperator class
        - output:
            * numpy array of shape (msh.x.size*msh.y.size, msh.x.size*msh.y.size),
              the image of the convection linear operator for the given concentration
        """
        output = np.zeros((self.shape[0], x_out.shape[1]))
        for i_col, col in enumerate(x_out.T):
            output[:, i_col] = self.matvec(col)
        return output
        # return np.hstack([self.matvec(col.reshape(-1, 1)) for col in x_out.T])
