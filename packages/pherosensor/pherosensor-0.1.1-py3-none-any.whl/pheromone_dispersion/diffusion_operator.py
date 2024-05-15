import numpy as np
from scipy.sparse.linalg import LinearOperator as LinOp


class Diffusion(LinOp):
    """
    Class containing the diffusion term linear operator of the PDE
    Subclass of the scipy.sparse.linalg.LinearOperator class,
    see https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.LinearOperator.html
    """

    def __init__(self, K, msh):
        """
        Instanciation of the class.

        - input:
            * K: object of the class DiffusionTensor
            * msh: object of the class MeshRect2D
        - attributes:
            * msh: object of the class MeshRect2D
            * K: object of the class DiffusionTensor
            * shape: tuple of integers, shape of the matrix of the linear operator
            * dtype: data type object, data type of the element of the matrix of the linear operator
        """

        self.msh = msh
        self.K = K
        self.shape = (self.msh.y.size * self.msh.x.size, self.msh.y.size * self.msh.x.size)
        self.dtype = np.dtype(float)

    def at_current_time(self, tc):
        """
        Update the attributes K of the class at a given time.

        - input:
            * tc: the current time
        """
        self.K.at_current_time(tc)

    def _matvec(self, x_out):
        """
        Compute the image (matrix-vector product) of the diffusion linear operator for a given (vector of) concentration

        - TO DO:
            * the gradient at msh.y[0] and msh.y[-1] at the vertical interfaces
              and at msh.x[0] and msh.x[-1] at the horizontal interfaces
              are not well taken into account
              phantom cells should be added that satisfies the boundary conditions
              for now, the solver works for diagonal diffusion tensor,
              i.e. for unidirectional wind field or for isotropic diffusion tensor (K_u=K_u_t)
        - input:
            * x_out:
                numpy array of (shape msh.x.size*msh.y.size, ),
                contains the concentration of pheromones raveled into a vector to match the format of the LinearOperator class
        - output:
            * numpy array of shape (msh.x.size*msh.y.size, ), the image of the convection linear operator for the given concentration
        """

        # reshape the vector (of (msh.x.size*msh.y.size, )) containg the concentration into a matrix (of shape (msh.y.size, msh.x.size))
        x = x_out.reshape((self.msh.y.size, self.msh.x.size))

        # Computation of the gradient of concentration on the vertical interfaces between the cells
        grad_at_vertical_interface = np.zeros((self.msh.y.size, self.msh.x_vertical_interface.size, 2))
        grad_at_vertical_interface[:, 1:-1, 0] = (x[:, 1:] - x[:, :-1]) / self.msh.dx
        grad_at_vertical_interface[1:-1, 1:-1, 1] = (x[2:, :-1] + x[2:, 1:] - (x[:-2, :-1] + x[:-2, 1:])) / (4 * self.msh.dy)
        # adding phantom cells, TO BE IMPROVED
        grad_at_vertical_interface[0, 1:-1, 1] = (x[1, :-1] + x[1, 1:] - (x[0, :-1] + x[0, 1:])) / (4 * self.msh.dy)
        grad_at_vertical_interface[-1, 1:-1, 1] = (x[-1, :-1] + x[-1, 1:] - (x[-2, :-1] + x[-2, 1:])) / (4 * self.msh.dy)

        # Computation of the gradient concentration on the horizontal interfaces between the cells
        grad_at_horizontal_interface = np.zeros((self.msh.y_horizontal_interface.size, self.msh.x.size, 2))
        grad_at_horizontal_interface[1:-1, 1:-1, 0] = (x[1:, 2:] + x[:-1, 2:] - (x[1:, :-2] + x[:-1, :-2])) / (4 * self.msh.dx)
        grad_at_horizontal_interface[1:-1, :, 1] = (x[1:, :] - x[:-1, :]) / self.msh.dy
        # adding phantom cells, TO BE IMPROVED
        grad_at_horizontal_interface[1:-1, 0, 0] = (x[1:, 1] + x[:-1, 1] - (x[1:, 0] + x[:-1, 0])) / (4 * self.msh.dx)
        grad_at_horizontal_interface[1:-1, -1, 0] = (x[1:, -1] + x[:-1, -1] - (x[1:, -2] + x[:-1, -2])) / (4 * self.msh.dx)

        # Computation of the horizontal flux going through the vertical interfaces
        flux_horizontal = np.zeros((self.msh.y.size, self.msh.x_vertical_interface.size))
        flux_horizontal[:, :] = (
            self.K.at_vertical_interface[:, :, 0, 0] * grad_at_vertical_interface[:, :, 0]
            + self.K.at_vertical_interface[:, :, 0, 1] * grad_at_vertical_interface[:, :, 1]
        )
        # Boundary Condition on the horizontal flux going through the vertical interfaces
        flux_horizontal[:, -1] = 0
        flux_horizontal[:, 0] = 0

        # Computation of the vertical flux going through the horizontal interfaces
        flux_vertical = np.zeros((self.msh.y_horizontal_interface.size, self.msh.x.size))
        flux_vertical[:, :] = (
            self.K.at_horizontal_interface[:, :, 1, 0] * grad_at_horizontal_interface[:, :, 0]
            + self.K.at_horizontal_interface[:, :, 1, 1] * grad_at_horizontal_interface[:, :, 1]
        )
        # Boundary Condition on the vertical flux going through the horizontal interfaces
        flux_vertical[0, :] = 0
        flux_vertical[-1, :] = 0

        # Computation of the total flux over the border of the cell for a cartesian mesh
        sum_faces = (
            self.msh.dy * (flux_horizontal[:, 1:] - flux_horizontal[:, :-1]) + self.msh.dx * (flux_vertical[1:, :] - flux_vertical[:-1, :])
        ) / self.msh.mass_cell
        return sum_faces.reshape((self.msh.y.size * self.msh.x.size,))

    def _matmat(self, x_out):
        """
        Compute the image (matrix-matrix product) of the diffusion linear operator for a given (matrix of) concentration

        - TO DO:
            * the gradient at msh.y[0] and msh.y[-1] at the vertical interfaces
              and at msh.x[0] and msh.x[-1] at the horizontal interfaces
              are not well taken into account
              phantom cells should be added that satisfies the boundary conditions
              for now, the solver works for diagonal diffusion tensor,
              i.e. for unidirectional wind field or for isotropic diffusion tensor (K_u=K_u_t)
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
