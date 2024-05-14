import numpy as np


class Mesh2D:
    """
    Class containing the generic 2D cartesian mesh
    TO BE IMPLEMENTED IF NEEDED
    """

    def __init__(self):
        None


class MeshRect2D:
    """
    Class containing a 2D rectangular cartesian mesh
    """

    def __init__(self, L_x, L_y, dx, dy, T_final, X_0=None):  #
        """
        Instanciation of the class.

        - TO BE DONE:
            * add exceptions to make sure that all the inputs are float
        - input:
            * L_x: float, length of the domain along the x-axis
            * L_y: float, length of the domain along the y-axis
            * dx: float, space step along the x-axis
            * dy: float, space step along the y-axis
            * T_final: float, final time of the modeling time window
            * X_0: coordinates of the origin of the mesh, is None if the orgin is (0, 0)
        - attributes:
            * L_x: float, length of the domain along the x-axis
            * L_y: float, length of the domain along the y-axis
            * dx: float, space step along the x-axis
            * dy: float, space step along the y-axis
            * x:
                numpy array of shape (L_x//dx, ), contains the x-coordinates of the center of the cells of the mesh
            * y:
                numpy array of shape (L_y//dy, ), contains the y-coordinates of the center of the cells of the mesh
            * x_vertical_interface:
                numpy array of shape (L_x//dx+1, ), contains the x-coordinates of the vertical interfaces between the cells of the mesh
            * y_horizontal_interface:
                numpy array of shape (L_y//dy+1, ), contains the y-coordinates of the horizontal interfaces between the cells of the mesh
            * mass_cell: float, contains the measure of a control volume
            * t: float, the current time of the modeling, initialized to 0
            * T_final: float, the final time of the modeling time window
            * X_0: coordinates of the origin of the mesh, is None if the orgin is (0, 0)
        """

        self.L_x = L_x
        self.L_y = L_y
        self.dx = dx
        self.dy = dy
        nx = L_x // dx
        ny = L_y // dy
        if dx - 1e-12 < L_x % dx:
            nx += 1
        if dy - 1e-12 < L_y % dy:
            ny += 1
        if X_0 is None:
            X_0 = (0.0, 0.0)
        self.x_vertical_interface = np.arange(0, (nx + 0.5) * dx, dx) + X_0[0]
        self.x = 0.5 * (self.x_vertical_interface[:-1] + self.x_vertical_interface[1:])
        self.y_horizontal_interface = np.arange(0, (ny + 0.5) * dy, dy) + X_0[1]
        self.y = 0.5 * (self.y_horizontal_interface[:-1] + self.y_horizontal_interface[1:])
        self.mass_cell = dx * dy

        self.t = 0
        self.T_final = T_final
        self.dt = None
        self.t_array = None

    def calc_dt_explicit_solver(self, U, mult_param=1.0, dt_max=0.1):
        """
        Make sure that the time step satisfies the CFL condition dt < 1 / (max(||U||) / (dx + dy))

        - TO BE DONE:
            * add exceptions to make sure that all the inputs are float
        - input:
            * U: object of the class Velocity
            * mult_param: multiplicative parameter that allows to enhance time accuracy by decreasing the time step (with mult_param<1)
            * dt_max: float, maximum time step
        - do:
            * store in the attribute dt the time step that satisfies the CFL condition and is smaller than the maximal time step 0.1
        """
        self.dt = np.min([1.0 / (1.2 * U.max_horizontal_U / self.dx + 1.2 * U.max_vertical_U / self.dy), dt_max]) * mult_param
        self.t_array = np.arange(0, self.T_final + self.dt, self.dt)
        self.T_final = self.t_array[-1]

    def calc_dt_implicit_solver(self, dt):
        """
        Make sure that the time step satisfies the CFL condition dt < 1 / (max(||U||) / (dx + dy))

        - TO BE DONE:
            * add exceptions to make sure that all the inputs are float
        - input:
            * U: object of the class Velocity
            * mult_param: multiplicative parameter that allows to enhance time accuracy by decreasing the time step (with mult_param<1)
            * dt_max: float, maximum time step
        - do:
            * store in the attribute dt the time step that satisfies the CFL condition and is smaller than the maximal time step 0.1
        """
        self.dt = dt
        self.t_array = np.arange(0, self.T_final + self.dt, self.dt)
        self.T_final = self.t_array[-1]
