import numpy as np
from scipy.sparse.linalg import LinearOperator as LinOp


class Reaction(LinOp):
    """
    Class containing the reaction term linear operator of the PDE
    Subclass of the scipy.sparse.linalg.LinearOperator class,
    see https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.LinearOperator.html
    """

    def __init__(self, reaction_coeff, msh):
        """
        Instanciation of the class.

        - input:
            * msh: object of the class MeshRect2D
            * reaction_coeff: array of shape (msh.y, msh.x), containing the reaction coefficient
        - attributes:
            * msh: object of the class MeshRect2D
            * reaction_coeff: array of shape (msh.y, msh.x)
            * shape: tuple of integers, shape of the matrix of the linear operator
            * dtype: data type object, data type of the element of the matrix of the linear operator
        """

        if reaction_coeff.shape != (msh.y.size, msh.x.size):
            raise ValueError("The shape of the deposition coefficient at the center of the cells does not match with the shape of the msh.")

        self.msh = msh
        self.reaction_coeff = reaction_coeff
        self.shape = (self.msh.y.size * self.msh.x.size, self.msh.y.size * self.msh.x.size)
        self.dtype = np.dtype(float)

    def update_reaction_coeff(self, reaction_coeff):
        """
        Update the attribute reaction_coeff with the value provide as input.

        - input:
            * reaction_coeff: the new values of the reaction coefficient
        """
        self.reaction_coeff = reaction_coeff

    def _matvec(self, x_out):
        """
        Compute the image (matrix-vector product) of the reaction linear operator for a given (vector of) concentration

        - input:
            * x_out:
                numpy array of shape (msh.x.size*msh.y.size, ),
                contains the concentration of pheromones raveled into a vector to match the format of the LinearOperator class
        - output:
            * numpy array of shape (msh.x.size*msh.y.size, ), the image of the convection linear operator for the given concentration
        """

        # reshape the vector (of (msh.x.size*msh.y.size, )) containg the concentration into a matrix (of shape (msh.y.size, msh.x.size))
        x = x_out.reshape((self.msh.y.size, self.msh.x.size))

        reaction = self.reaction_coeff * x
        return reaction.reshape((self.msh.y.size * self.msh.x.size,))

    def _matmat(self, x_out):
        """
        Compute the image (matrix-matrix product) of the reaction linear operator for a given (matrix of) concentration

        - input:
            * x_out:
                numpy array of (shape msh.x.size*msh.y.size, msh.x.size*msh.y.size),
                contains the concentration of pheromones raveled into a vector to match the format of the LinearOperator class
        - output:
            * numpy array of shape (msh.x.size*msh.y.size, msh.x.size*msh.y.size),
              the image of the convection linear operator for the given concentration
        """

        # x = x_out.reshape((self.msh.y.size,self.msh.x.size,x_out.shape[-1]))
        # reaction = self.reaction_coeff[:,:,None] * x
        # return reaction.reshape((self.msh.y.size * self.msh.x.size,x_out.shape[-1]))
        output = np.zeros((self.shape[0], x_out.shape[1]))
        for i_col, col in enumerate(x_out.T):
            output[:, i_col] = self.matvec(col)
        return output
        # return np.hstack([self.matvec(col.reshape(-1, 1)) for col in x_out.T])
