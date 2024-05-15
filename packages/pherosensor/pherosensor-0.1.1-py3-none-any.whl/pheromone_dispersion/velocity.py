from datetime import timedelta
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.interpolate import LinearNDInterpolator as interp2d
from scipy.interpolate import interp1d


class Velocity:
    """
    Class containing the velocity field
    """

    def __init__(self, msh, U_at_vertical_interface, U_at_horizontal_interface, t=None):
        """
        Instanciation of the class.

        - TO BE DONE:
            * adapt to some more realistic input (e.g. velocity field inside the cells ...)
        - input:
            * msh: object of the class MeshRect2D
            * U_at_vertical_interface:
                numpy array of shape (t.size, mesh.y.size, mesh.vx.size, 2),
                contains the velocity field on the vertical interfaces of the cells
            * U_at_horizontal_interface:
                numpy array of shape (t.size, mesh.vy.size, mesh.x.size, 2),
                contains the velocity field on the horizontal interfaces of the cells
            * t: numpy array, the vector containing the times at which the velocity is given, if None, the velocity is supposed steady
        - attributes:
            * at_vertical_interface:
                numpy array of shape (mesh.y, mesh.vx, 2), contains the velocity field on the vertical interfaces of the cells
            * at_horizontal_interface:
                numpy array of shape (mesh.vy, mesh.x, 2), contains the velocity field on the horizontal interfaces of the cells
            * div: array of shape (mesh.y.size, mesh.x.size), contains the divergence of U at the center of the cells at the current time
            * t: numpy array, the vector containing the times at which the velocity is given, if None, the velocity is supposed steady
            * time_interpolation_at_vertical_interface:
                object of the class scipy.interpolate.interp1D,
                aims at computing the velocity at the vertical interfaces given a time using the linear interpolation of the data
            * time_interpolation_at_horizontal_interface:
                object of the class scipy.interpolate.interp1D,
                aims at computing the velocity at the horizontal interfaces given a time using the linear interpolation of the data
            * time_interpolation_div:
                object of the class scipy.interpolate.interp1D,
                aims at computing the divergence of the velocity given a time using the linear interpolation of the data
            * cell_above_upwind: array of boolean, is True if the cell above is the upwind cell for the y-component of the wind velocity
            * cell_under_upwind: array of boolean, is True if the cell under is the upwind cell for the y-component of the wind velocity
            * cell_right_upwind: array of boolean, is True if the right cell is the upwind cell for the x-component of the wind velocity
            * cell_left_upwind: array of boolean, is True if the left cell under is the upwind cell for the x-component of the wind velocity
            * max_U_horizontal_U: float, L^infinity norm of the horizontal component of the velocity field
            * max_U_vertical_U: float, L^infinity norm of the vertical component of the velocity field
        """
        self.t = t

        if self.t is not None:
            if U_at_horizontal_interface.ndim != 4 or U_at_vertical_interface.ndim != 4:
                raise ValueError(
                    "The number dimension of the velocity field is incorrect,"
                    + " the velocity field is unsteady,"
                    + " the number of dimension shoud be 3"
                )
            if self.t.size != U_at_vertical_interface.shape[0] or self.t.size != U_at_horizontal_interface.shape[0]:
                raise ValueError("The shape of the velocity field does not coincide with the shape of the time vector")
            div_U_all_t = ((U_at_horizontal_interface[:, 1:, :, 1] - U_at_horizontal_interface[:, :-1, :, 1]) / msh.dy) + (
                (U_at_vertical_interface[:, :, 1:, 0] - U_at_vertical_interface[:, :, :-1, 0]) / msh.dx
            )
            self.at_vertical_interface = U_at_vertical_interface[0, :, :, :]
            self.at_horizontal_interface = U_at_horizontal_interface[0, :, :, :]
            self.div = div_U_all_t[0, :, :]
            self.time_interpolation_at_vertical_interface = interp1d(t, U_at_vertical_interface, axis=0)
            self.time_interpolation_at_horizontal_interface = interp1d(t, U_at_horizontal_interface, axis=0)
            self.time_interpolation_div = interp1d(t, div_U_all_t, axis=0)
            self.max_horizontal_U = np.max(
                (np.max(np.abs(U_at_vertical_interface[:, :, :, 0])), np.max(np.abs(U_at_horizontal_interface[:, :, :, 0])))
            )
            self.max_vertical_U = np.max(
                (np.max(np.abs(U_at_vertical_interface[:, :, :, 1])), np.max(np.abs(U_at_horizontal_interface[:, :, :, 1])))
            )
            self.min_norm = np.min(np.linalg.norm(U_at_vertical_interface, axis=3))
            self.max_norm = np.max(np.linalg.norm(U_at_vertical_interface, axis=3))

        else:
            if U_at_horizontal_interface.ndim != 3 or U_at_vertical_interface.ndim != 3:
                raise ValueError(
                    "The number dimension of the velocity field is incorrect,"
                    + " the velocity field is unsteady,"
                    + " the number of dimension shoud be 2"
                )
            self.at_vertical_interface = U_at_vertical_interface
            self.at_horizontal_interface = U_at_horizontal_interface
            self.div = ((self.at_horizontal_interface[1:, :, 1] - self.at_horizontal_interface[:-1, :, 1]) / msh.dy) + (
                (self.at_vertical_interface[:, 1:, 0] - self.at_vertical_interface[:, :-1, 0]) / msh.dx
            )
            self.max_horizontal_U = np.max((np.max(U_at_vertical_interface[:, :, 0]), np.max(U_at_horizontal_interface[:, :, 0])))
            self.max_vertical_U = np.max((np.max(U_at_vertical_interface[:, :, 1]), np.max(U_at_horizontal_interface[:, :, 1])))

        self.cell_above_upwind = self.at_horizontal_interface[:, :, 1] < 0
        self.cell_under_upwind = self.at_horizontal_interface[:, :, 1] > 0
        self.cell_right_upwind = self.at_vertical_interface[:, :, 0] < 0
        self.cell_left_upwind = self.at_vertical_interface[:, :, 0] >= 0

        if self.at_vertical_interface.shape != (msh.y.size, msh.x_vertical_interface.size, 2):
            raise ValueError(
                "The shape of the velocity field at the vertical and horizontal interfaces do not match with the shape of the msh."
            )
        if (
            self.at_vertical_interface.shape[0] + 1 != self.at_horizontal_interface.shape[0]
            or self.at_horizontal_interface.shape[1] + 1 != self.at_vertical_interface.shape[1]
        ):
            raise ValueError(
                "The shape of the velocity field at the vertical interfaces"
                + "(that is (nb of cells along the y axis, nb of cells along the x axis + 1)) "
                + "does not coincide with the shape of the velocity field at the horizontal interfaces"
                + "(that is (nb of cells along the y axis + 1, nb of cells along the x axis))."
            )

    def at_current_time(self, tc):
        """
        Update the attributes div, at_vertical_interface and at_horizontal_interface of the class at a given time using linear interpolation
        and re-compute the attributes cell_above_upwind, cell_under_upwind, cell_right_upwind and cell_left_upwind

        - input:
            * tc: float, the current time
        """

        if self.t is not None:
            if tc < min(self.t) or tc > max(self.t):
                raise ValueError("The given time must be between the lowest and largest times contained in the time vector.")
            self.at_vertical_interface = self.time_interpolation_at_vertical_interface(tc)
            self.at_horizontal_interface = self.time_interpolation_at_horizontal_interface(tc)
            self.div = self.time_interpolation_div(tc)
            self.cell_above_upwind = self.at_horizontal_interface[:, :, 1] < 0
            self.cell_under_upwind = self.at_horizontal_interface[:, :, 1] >= 0
            self.cell_right_upwind = self.at_vertical_interface[:, :, 0] < 0
            self.cell_left_upwind = self.at_vertical_interface[:, :, 0] >= 0


def velocity_field_from_meteo_data(path_data, file_name_data, msh):
    """
    read the meteorological wind velocity data
    and return a object of the Velocity class
    containing the linear interpolation of these data on the mesh

    - input:
        * path_data: str, path to the folder that contains the meteorological data
        * file_name_data: str, name of the file that contains the meteorological data
        * msh: object of the class MeshRect2D
    - output:
        * Velocity object
    - TO DO :
        * add exceptions to check path and file names,
                         to check the data have the expected format,
                         to check the msh,
                         to check that the mesh is covered by the data
    """
    df = pd.read_csv(Path(path_data) / file_name_data)

    nb_times = len(df['step'].unique())
    t = np.zeros((nb_times,))
    U_at_vertical_interface = np.zeros((nb_times, msh.y.size, msh.x_vertical_interface.size, 2))
    U_at_horizontal_interface = np.zeros((nb_times, msh.y_horizontal_interface.size, msh.x.size, 2))

    xx_at_vertical_interface, yy_at_vertical_interface = np.meshgrid(msh.x_vertical_interface, msh.y)
    xx_at_horizontal_interface, yy_at_horizontal_interface = np.meshgrid(msh.x, msh.y_horizontal_interface)

    for i_step, step in enumerate(df['step'].unique()):
        d, _, hms = step.split(" ")
        h, m, s = hms.split(":")
        t[i_step] = timedelta(days=int(d), seconds=int(s), minutes=int(m), hours=int(h)).total_seconds()

        df_tc = df.loc[df['step'] == step]
        interp_u = interp2d(list(zip(df_tc['X'], df_tc['Y'])), df_tc['u10'])
        interp_v = interp2d(list(zip(df_tc['X'], df_tc['Y'])), df_tc['v10'])

        U_at_vertical_interface[i_step, :, :, 0] = interp_u(xx_at_vertical_interface, yy_at_vertical_interface)
        U_at_vertical_interface[i_step, :, :, 1] = interp_v(xx_at_vertical_interface, yy_at_vertical_interface)

        U_at_horizontal_interface[i_step, :, :, 0] = interp_u(xx_at_horizontal_interface, yy_at_horizontal_interface)
        U_at_horizontal_interface[i_step, :, :, 1] = interp_v(xx_at_horizontal_interface, yy_at_horizontal_interface)

    return Velocity(msh, U_at_vertical_interface, U_at_horizontal_interface, t=t)
