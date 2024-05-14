import numpy as np
from scipy.sparse.linalg import LinearOperator as LinOp


class Id(LinOp):
    """
    Class containing the identity operator of the PDE
    Subclass of the scipy.sparse.linalg.LinearOperator class,
    see https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.LinearOperator.html
    """

    def __init__(self, msh):
        """
        Instanciation of the class.

        - input:
            * msh: object of the class MeshRect2D
        - attributes:
            * shape: tuple of integers, shape of the matrix of the linear operator
            * dtype: data type object, data type of the element of the matrix of the linear operator
        """
        self.shape = (msh.y.size * msh.x.size, msh.y.size * msh.x.size)
        self.dtype = np.dtype(float)

    def _matvec(self, x_out):
        """
        Compute the image (matrix-vector product) of the reaction linear operator for a given (vector of) concentration

        - TO BE DONE:
            * Better implementation or already implemented in scipy?
        - input:
            * x_out:
                numpy array of shape (shape msh.x.size*msh.y.size, ),
                contains the concentration of pheromones raveled into a vector to match the format of the LinearOperator class
        - output:
            * numpy array of shape (msh.x.size*msh.y.size, ), the image of the identity operator for the given concentration
        """
        return x_out
