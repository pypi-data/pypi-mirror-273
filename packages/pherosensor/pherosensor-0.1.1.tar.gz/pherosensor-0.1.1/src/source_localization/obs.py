import numpy as np
import scipy.sparse as sps


class Obs:
    """
    Class containing:
    - the observations: its value, the time and space location of the observations,
    - the corresponding estimation of the observed variable (accumulation of pheromone over a time window) computed by the direction model
    - the observations error covariance matrix
    - the observation operator and the adjoint operator of its derivative with respect of the state variable
    """

    def __init__(self, t_obs, X_obs, d_obs, msh, index_sensor=None, dt_obs_operator=0.0):
        """
        Instanciation of the class.

        - TO DO:
            * update the documentation and comments for the new observation operator
            * add an exception to make sure that the accumulation time window does not overlapp for a given sensor
            * add an exception to make sure that no observations are made after
        - input:
            * t_obs: array of the shape (N_obs,), contains the observations times
            * X_obs: array of the shape (N_obs,2), contains the locations of the observations
            * d_obs: array of the shape (N_obs,), contains the values of the observations
            * msh: object of the class MeshRect2D
        - attributes:
            * msh: object of the class MeshRect2D
            * t_obs: array of the shape (N_obs,), contains the observations times
            * X_obs: array of the shape (N_obs,2), contains the locations of the observations
            * d_obs: array of the shape (N_obs,), contains the values of the observations
            * N_obs: int, contains the number of observations
            * X_sensors: array of tuple, contains the position of the sensors
            * nb_sensors: int, contains the number of sensors
            * dt_obs_operator: float, contains the length of the time window of accumulation
            * nb_dt_in_obs_time_window: int, contains the number of time steps covering the time window of accumulation
            * c_est:
                array of the shape (N_obs, nb_dt_in_obs_time_window),
                contains the estimation of the state variable (concentration) computed by the direct model
                at the time and space location required to estimate the observed variable at the time and space location of the observations
            * d_est:
                array of the shape (N_obs,),
                contains the estimation of the observed variable (accumulation of pheromone) computed by the direct model
                at the time and space location of the observations
            * R_inv:
                array of shape (N_obs, N_obs), contains the inverse of the observations error covariance matrix, by default the identity
            * index_obs_to_index_time_est:
                array of shape (N_obs, nb_dt_in_obs_time_window),
                contains the indexes of the times at which the state variable is required to compute the observation variable
                given the index of an observation
            * index_time_est_to_index_obs:
                dictionnary,
                for a time as key, contains the array of index of the observations
                that require the estimate of the state variable at this time to estimate the observed variable
        """

        self.msh = msh
        self.t_obs = np.copy(t_obs)
        self.X_obs = np.copy(X_obs)
        self.d_obs = np.copy(d_obs)
        self.N_obs = np.size(d_obs)

        if self.msh.t_array is None:
            raise ValueError(
                "The array containing the time at which the direct model is solved, has not been correctly initialized."
                + " This is probably because the time step has not been computed so the CFL condition is satisfied."
                + " The method calc_CFL of the class MeshRect2D should then be executed first."
            )

        if d_obs.ndim != 1:
            raise ValueError("The array of the observations should have just one dimension, it should not be a matrix.")

        if t_obs.shape != (self.N_obs,):
            raise ValueError(
                "The number of observations and the number of observations time are not the same."
                + " Either the vector of observations or the vector of time are incomplete."
            )
        if np.max(t_obs) > np.max(self.msh.t_array) or np.min(t_obs) < np.min(self.msh.t_array):
            raise ValueError(
                "At least one of the observations is made out of the temporal domain."
                + " Make sure that the observation times are inside the modelling time window."
            )

        if X_obs.shape != (self.N_obs, 2):
            raise ValueError(
                " The number of observations and the number of location of observations are not the same."
                + " Either the vector of observations or the vector of location are incomplete."
            )
        if (
            np.max(self.X_obs[:, 0]) > np.max(self.msh.x_vertical_interface)
            or np.min(self.X_obs[:, 0]) < np.min(self.msh.x_vertical_interface)
            or np.max(self.X_obs[:, 1]) > np.max(self.msh.y_horizontal_interface)
            or np.min(self.X_obs[:, 1]) < np.min(self.msh.y_horizontal_interface)
        ):
            raise ValueError(
                "At least one of the observations is made out of the spatial domain."
                + " Make sure that the observation location are inside the domain."
            )

        # initialization of the vector containing the position of the sensors
        self.X_sensors = np.unique(self.X_obs, axis=0)
        self.nb_sensors = np.shape(self.X_sensors)[0]

        self.dt_obs_operator = dt_obs_operator
        self.nb_dt_in_obs_time_window = int((self.dt_obs_operator // self.msh.dt) + 1)
        if np.min(self.t_obs) < self.dt_obs_operator:
            raise ValueError(
                "The time window of integration of the observation operator for the first observation starts before the temporal domain."
                + " This is probably because the integration time window is too large or the observation times are inaccurate."
            )
        # Exception to make sure that the accumulation time windows do not overlapp for a given sensor
        for X_sensor in self.X_sensors:
            indexes_sensor = [x == X_sensor[0] and y == X_sensor[1] for x, y in zip(self.X_obs[:, 0], self.X_obs[:, 1])]
            # indexes_sensor = np.where(self.X_obs==X_sensor)
            ts_obs_sensor = self.t_obs[indexes_sensor]
            for t_obs_sensor in ts_obs_sensor:
                if (np.abs(ts_obs_sensor[ts_obs_sensor != t_obs_sensor] - t_obs_sensor) < self.dt_obs_operator).any():
                    raise ValueError(
                        "The time windows of integration for two different data of a same sensors are overlapping."
                        + "The implemented observation operator supposes that these time windows are not overlapping"
                    )

        self.c_est = np.full((self.N_obs, self.nb_dt_in_obs_time_window), np.nan)
        self.d_est = np.full((self.N_obs,), np.nan)
        self.R_inv = sps.identity(self.N_obs, dtype=int)

        # initialization of the vector containing the time index given the index of an observation
        self.index_obs_to_index_time_est = np.full((self.N_obs, self.nb_dt_in_obs_time_window), np.nan)
        self.index_obs_to_index_time_est[:, 0] = np.argmin(
            np.abs(self.t_obs.reshape((self.N_obs, 1)) - msh.t_array.reshape((1, msh.t_array.size))), axis=1
        )
        for i in range(1, self.nb_dt_in_obs_time_window):
            self.index_obs_to_index_time_est[:, i] = self.index_obs_to_index_time_est[:, i - 1] - 1

        # initialization of the dictionnary containing the indexes of the observations given the time index
        self.index_time_est_to_index_obs = {}
        for i in range(self.nb_dt_in_obs_time_window):
            for increment, time_idx in enumerate(self.index_obs_to_index_time_est[:, i]):
                if time_idx in self.index_time_est_to_index_obs.keys():
                    self.index_time_est_to_index_obs[time_idx].append(increment)
                else:
                    self.index_time_est_to_index_obs[time_idx] = [increment]

    def obs_operator(self):
        """
        the observation operator
        i.e. integration of the state variable of the direct model over the time window [t_obs-dt_obs_operator; t_obs]
        assuming that the integration time window for different data of a same sensor are not overlapping

        - do:
            * compute an estimation of the observed variable given an estimation of the state variable of the direct model
            * store the estimation of the observed variable in the attribute d_est
        """

        if np.array([np.isnan(self.c_est[i]) for i in range(self.N_obs)]).any():
            raise ValueError(
                "The vector of estimation of the state variable at the observations time and location has not been computed."
                + " The method solver_est_at_obs_times should be used to computed this vector."
            )
        self.d_est = np.sum(self.c_est, axis=1) * self.msh.dt

    def onesensor_adjoint_derivative_obs_operator(self, t, delta_c, index_sensor):
        """
        compute the spatial map of the adjoint of the derivative of the observation operator with respect to the state variable
        at a given time

        - input:
            * t: the current time
            * delta_c: numpy array of shape (N_obs, ), element of the space of the concentration (state variable)
            * index_sensor:
                int, index of the sensor to consider in the solving the one-sensor adjoint model
        - output:
            * numpy array of shape (msh.x.size*msh.y.size, ),
                evaluation of the adjoint of the derivative of the observation operator in delta_c
        """
        index_t = np.argmin(np.abs(t - self.msh.t_array))
        out = np.zeros((self.msh.y.size, self.msh.x.size))
        X_sensor = self.X_sensors[index_sensor]
        if index_t in self.index_obs_to_index_time_est:
            index_obs_current_t = self.index_time_est_to_index_obs[index_t]
            X_obs_current_t = self.X_obs[index_obs_current_t]
            if X_sensor in X_obs_current_t:
                index = np.argmin(np.abs(X_obs_current_t[:, 0] - X_sensor[0]) + np.abs(X_obs_current_t[:, 1] - X_sensor[1]))
                index_obs = index_obs_current_t[index]
                index_x_est = np.argmin(np.abs(self.msh.x - X_sensor[0]))
                index_y_est = np.argmin(np.abs(self.msh.y - X_sensor[1]))
                out[index_y_est, index_x_est] = delta_c[index_obs] * self.msh.dt
        return out.reshape((self.msh.y.size * self.msh.x.size,))

    def adjoint_derivative_obs_operator(self, t, delta_c):
        """
        compute the spatial map of the adjoint of the derivative of the observation operator with respect to the state variable
        at a given time

        - input:
            * t: the current time
            * delta_c: numpy array of shape (N_obs, ), element of the space of the concentration (state variable)
        - output:
            * numpy array of shape (msh.x.size*msh.y.size, ),
                evaluation of the adjoint of the derivative of the observation operator in delta_c
        """
        index_t = np.argmin(np.abs(t - self.msh.t_array))
        out = np.zeros((self.msh.y.size, self.msh.x.size))
        # update only if an observation is made at the current time
        # if no observation is made at the current time, the attribute index_x_est is set to []
        if index_t in self.index_obs_to_index_time_est:
            # initialization of index_y_est
            index_x_est = []
            index_y_est = []
            # extracting the indexes of the observations made at the current time
            index_obs = self.index_time_est_to_index_obs[index_t]
            # looping on the observations made at the current time and storing the indexes of the coordinates of the estimate points
            for i in index_obs:
                index_x_est.append(np.argmin(np.abs(self.msh.x - self.X_obs[i, 0])))
                index_y_est.append(np.argmin(np.abs(self.msh.y - self.X_obs[i, 1])))

            # for each observation points, store the associated input at the correponding estimate point
            for i_x, i_y, i_obs in zip(index_x_est, index_y_est, index_obs):
                out[i_y, i_x] = delta_c[i_obs] * self.msh.dt
        return out.reshape((self.msh.y.size * self.msh.x.size,))
