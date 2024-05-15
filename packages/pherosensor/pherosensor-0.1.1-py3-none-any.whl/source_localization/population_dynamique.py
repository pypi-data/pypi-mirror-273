import numpy as np
from scipy.sparse.linalg import LinearOperator as LinOp


class StationnaryPopulationDynamicModel(LinOp):
    """
    Class containing the time derivative operator of the control
    Subclass of the scipy.sparse.linalg.LinearOperator class,
    see https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.LinearOperator.html
    """

    """
    TO DO :
    find a way to make sure that the derivative can be computed, i.e. there is enough time and space points
    """

    def __init__(self, msh):
        """
        Instanciation of the class.

        - input:
        - attributes:
            * shape: tuple of integers, shape of the matrix of the linear operator
            * dtype: data type object, data type of the element of the matrix of the linear operator
        """
        self.msh = msh
        self.shape = (
            self.msh.y.size * self.msh.x.size * (self.msh.t_array.size - 1),
            self.msh.y.size * self.msh.x.size * self.msh.t_array.size,
        )
        self.dtype = np.dtype(float)

    def _matvec(self, x_out):
        """
        Compute the image (matrix-vector product) of the time derivative operator for a given vector of source

        - input:
            * x_out:
                numpy array of shape (msh.x.size*msh.y.size*msh.t_array.size, ),
                contains the source raveled into a vector to match the format of the LinearOperator class
        - output:
            * numpy array of shape (msh.x.size*msh.y.size*msh.t_array.size, ),
                the image of the time derivative operator for a given source
        """
        S = x_out.reshape((self.msh.t_array.shape[0], self.msh.y.shape[0], self.msh.x.shape[0]))

        # time derivative of the S

        # d_tS = np.zeros((self.msh.t_array.shape[0], self.msh.y.shape[0], self.msh.x.shape[0]))
        # d_tS[0, :, :] = S[1, :, :] - S[0, :, :]
        # d_tS[-1, :, :] = S[-1, :, :] - S[-2, :, :]
        # d_tS[1:-1, :, :] = (S[2:, :, :] - S[:-2, :, :]) / 2

        d_tS = np.zeros((self.msh.t_array.shape[0] - 1, self.msh.y.shape[0], self.msh.x.shape[0]))
        d_tS = S[1:, :, :] - S[:-1, :, :]

        return d_tS.reshape((self.msh.y.size * self.msh.x.size * (self.msh.t_array.size - 1),)) / self.msh.dt

    def _rmatvec(self, x_out):
        """
        Compute the image (matrix-vector product) of the adjoint of the time derivative operator for a given vector of source

        - input:
            * x_out:
                numpy array of shape (msh.x.size*msh.y.size*msh.t_array.size, ),
                contains the source raveled into a vector to match the format of the LinearOperator class
        - output:
            * numpy array of shape (msh.x.size*msh.y.size*msh.t_array.size, ),
                the image of the adjoint of the time derivative operator for a given source
        """
        S = x_out.reshape((self.msh.t_array.shape[0] - 1, self.msh.y.shape[0], self.msh.x.shape[0]))

        # time derivative of the S

        # d_tS_adjoint = np.zeros((self.msh.t_array.shape[0], self.msh.y.shape[0], self.msh.x.shape[0]))
        # d_tS_adjoint[0, :, :] = -0.5 * S[1, :, :] - S[0, :, :]
        # d_tS_adjoint[1, :, :] = -0.5 * S[2, :, :] + S[0, :, :]
        # d_tS_adjoint[-1, :, :] = S[-1, :, :] + 0.5 * S[-2, :, :]
        # d_tS_adjoint[-2, :, :] = -S[-1, :, :] + 0.5 * S[-3, :, :]
        # d_tS_adjoint[2:-2, :, :] = (-S[3:-1, :, :] + S[1:-3, :, :]) / 2

        d_tS_adjoint = np.zeros((self.msh.t_array.shape[0], self.msh.y.shape[0], self.msh.x.shape[0]))
        d_tS_adjoint[0, :, :] = -S[0, :, :]
        d_tS_adjoint[1:-1, :, :] = -S[1:, :, :] + S[:-1, :, :]
        d_tS_adjoint[-1, :, :] = S[-1, :, :]

        return d_tS_adjoint.reshape((self.msh.y.size * self.msh.x.size * self.msh.t_array.size,)) / self.msh.dt


class PopulationDynamicModel(LinOp):
    """
    Class containing the time derivative operator of the control
    Subclass of the scipy.sparse.linalg.LinearOperator class,
    see https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.LinearOperator.html
    """

    def __init__(self, msh, death_rate=0.1):
        """
        Instanciation of the class.

        - input:
        - attributes:
            * shape: tuple of integers, shape of the matrix of the linear operator
            * dtype: data type object, data type of the element of the matrix of the linear operator
        """
        self.msh = msh
        if isinstance(death_rate, float):
            self.death_rate = death_rate * np.ones((self.msh.t_array.shape[0], self.msh.y.shape[0], self.msh.x.shape[0]))
        elif isinstance(death_rate, np.ndarray):
            self.death_rate = death_rate
        elif death_rate is None:
            self.death_rate = np.zeros((self.msh.t_array.shape[0], self.msh.y.shape[0], self.msh.x.shape[0]))
        self.shape = (
            self.msh.y.size * self.msh.x.size * (self.msh.t_array.size - 1),
            self.msh.y.size * self.msh.x.size * self.msh.t_array.size,
        )
        self.dtype = np.dtype(float)

    def _matvec(self, x_out):
        """
        Compute the image (matrix-vector product) of the time derivative operator for a given vector of source

        - input:
            * x_out:
                numpy array of shape (msh.x.size*msh.y.size*msh.t_array.size, ),
                contains the source raveled into a vector to match the format of the LinearOperator class
        - output:
            * numpy array of shape (msh.x.size*msh.y.size*msh.t_array.size, ),
                the image of the time derivative operator for a given source
        """
        S = x_out.reshape((self.msh.t_array.shape[0], self.msh.y.shape[0], self.msh.x.shape[0]))
        res = (S[1:, :, :] - S[:-1, :, :]) / self.msh.dt
        res += np.multiply(self.death_rate[1:, :, :], S[1:, :, :])
        return res.reshape((self.msh.y.size * self.msh.x.size * (self.msh.t_array.size - 1),))

    def _rmatvec(self, x_out):
        """
        Compute the image (matrix-vector product) of the adjoint of the time derivative operator for a given vector of source

        - input:
            * x_out:
                numpy array of shape (msh.x.size*msh.y.size*msh.t_array.size, ),
                contains the source raveled into a vector to match the format of the LinearOperator class
        - output:
            * numpy array of shape (msh.x.size*msh.y.size*msh.t_array.size, ),
                the image of the adjoint of the time derivative operator for a given source
        """
        S = x_out.reshape((self.msh.t_array.shape[0] - 1, self.msh.y.shape[0], self.msh.x.shape[0]))
        res = np.zeros((self.msh.t_array.shape[0], self.msh.y.shape[0], self.msh.x.shape[0]))
        res[0, :, :] = -S[0, :, :] / self.msh.dt
        res[1:-1, :, :] = (-S[1:, :, :] + S[:-1, :, :]) / self.msh.dt
        res[-1, :, :] = S[-1, :, :] / self.msh.dt
        res[1:, :, :] += np.multiply(self.death_rate[1:, :, :], S)

        return res.reshape((self.msh.y.size * self.msh.x.size * self.msh.t_array.size,))
