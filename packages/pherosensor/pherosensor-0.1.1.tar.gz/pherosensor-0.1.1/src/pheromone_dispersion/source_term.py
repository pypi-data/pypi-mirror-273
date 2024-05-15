from scipy.interpolate import interp1d as interp


class Source:
    """
    Class containing the source term of the PDE
    Subclass of the scipy.sparse.linalg.LinearOperator class,
    see https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.LinearOperator.html
    """

    def __init__(self, msh, value, t=None):
        """
        Instanciation of the class.

        - input:
            * msh: object of the class MeshRect2D
            * value: numpy array of shape (t.size, msh.y.size, msh.x.size,), contains the matrix the coefficient of the source term
            * t: numpy array, the vector containing the times at which the source is given, if None, the source is supposed steady
        - attributes:
            * t: numpy array, the vector containing the times at which the source is given, if None, the source is supposed steady
            * value:
                numpy array of shape (t.size, mesh.y.size, mesh.x.size,),
                contains the discharge of pheromones in the air by the source of emissions
            * time_interpolation:
                object of the class scipy.interpolate.interp1D,
                aims at computing the source term given the current time using the linear interpolation of the data
        """

        self.t = t
        if self.t is not None:
            if value.ndim != 3:
                raise ValueError(
                    "The number dimension of the source term is incorrect, the source term is unsteady, the number of dimension shoud be 3"
                )
            if self.t.size != value.shape[0]:
                raise ValueError("The shape of the source term does not coincide with the shape of the time vector")
            self.value = value[0, :, :]
            self.time_interpolation = interp(t, value, axis=0)
        else:
            if value.ndim != 2:
                raise ValueError(
                    "The number dimension of the source term is incorrect, the source term is steady, the number of dimension shoud be 2"
                )
            self.value = value
            self.t = None

        if self.value.shape[0] != msh.y.size or self.value.shape[1] != msh.x.size:
            raise ValueError("The shape of the source term at the center of the cells does not match with the shape of the msh.")

    def at_current_time(self, tc):
        """
        Update the attributes S of the class at a given time using linear interpolation.

        - input:
            * tc: the current time
        """

        if self.t is not None:
            if tc < min(self.t) or tc > max(self.t):
                raise ValueError("The given time must be between the lowest and largest times contained in the time vector.")
            self.value = self.time_interpolation(tc)
