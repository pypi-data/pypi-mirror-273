import numpy as np


class DiffusionTensor:
    """
    Class containing the anisotropic and inhomogeneous diffusion tensor
    """

    def __init__(self, U, K_u, K_u_t):
        """
        Instanciation of the class.

        - TO BE DONE:
            * add exceptions to make sure that all the inputs have the right type
        - input:
            * U: object of the class Velocity
            * K_u: float, the diffusion coefficient in the wind direction
            * K_u_t: float, the diffusion coefficient in the crosswind direction
        - attributes:
            * U: object of the class Velocity
            * at_vertical_interface:
                numpy array of shape (msh.y, msh.x_vertical_interface, 2, 2), contains the diffusion tensor at each vertical interfaces
            * at_horizontal_interface:
                numpy array of shape (msh.y_horizontal_interface, msh.x, 2, 2), contains the diffusion tensor at each horizontal interfaces
            * K_u: float, the diffusion coefficient in the wind direction
            * K_u_t: float, the diffusion coefficient in the crosswind direction
        """
        self.U = U
        self.K_u = K_u
        self.K_u_t = K_u_t
        self.diffusion_tensor_from_velocity_field()

    def diffusion_tensor_from_velocity_field(self):
        """
        Compute diffusion tensor from the velocity field using the following rotation formula:
        K = K_u_t*Id_(2,2) - (K_u_t - K_u)* U.U^T / ||U||^2
        """

        # On the vertical interfaces of the mesh
        norm_U_at_vertical_interface = np.linalg.norm(self.U.at_vertical_interface, axis=2)
        U_at_vertical_interface = self.U.at_vertical_interface / norm_U_at_vertical_interface[:, :, None]
        self.at_vertical_interface = np.zeros((U_at_vertical_interface.shape[0], U_at_vertical_interface.shape[1], 2, 2))
        self.at_vertical_interface[:, :, 0, 0] = self.K_u_t
        self.at_vertical_interface[:, :, 1, 1] = self.K_u_t
        self.at_vertical_interface[:, :, 0, 0] += (
            -(self.K_u_t - self.K_u) * U_at_vertical_interface[:, :, 0] * U_at_vertical_interface[:, :, 0]
        )
        self.at_vertical_interface[:, :, 0, 1] += (
            -(self.K_u_t - self.K_u) * U_at_vertical_interface[:, :, 0] * U_at_vertical_interface[:, :, 1]
        )
        self.at_vertical_interface[:, :, 1, 0] += (
            -(self.K_u_t - self.K_u) * U_at_vertical_interface[:, :, 0] * U_at_vertical_interface[:, :, 1]
        )
        self.at_vertical_interface[:, :, 1, 1] += (
            -(self.K_u_t - self.K_u) * U_at_vertical_interface[:, :, 1] * U_at_vertical_interface[:, :, 1]
        )

        # On the horizontal interfaces of the mesh
        norm_U_at_horizontal_interface = np.linalg.norm(self.U.at_horizontal_interface, axis=2)
        U_at_horizontal_interface = self.U.at_horizontal_interface / norm_U_at_horizontal_interface[:, :, None]
        self.at_horizontal_interface = np.zeros((U_at_horizontal_interface.shape[0], U_at_horizontal_interface.shape[1], 2, 2))
        self.at_horizontal_interface[:, :, 0, 0] = self.K_u_t
        self.at_horizontal_interface[:, :, 1, 1] = self.K_u_t
        self.at_horizontal_interface[:, :, 0, 0] += (
            -(self.K_u_t - self.K_u) * U_at_horizontal_interface[:, :, 0] * U_at_horizontal_interface[:, :, 0]
        )
        self.at_horizontal_interface[:, :, 0, 1] += (
            -(self.K_u_t - self.K_u) * U_at_horizontal_interface[:, :, 0] * U_at_horizontal_interface[:, :, 1]
        )
        self.at_horizontal_interface[:, :, 1, 0] += (
            -(self.K_u_t - self.K_u) * U_at_horizontal_interface[:, :, 0] * U_at_horizontal_interface[:, :, 1]
        )
        self.at_horizontal_interface[:, :, 1, 1] += (
            -(self.K_u_t - self.K_u) * U_at_horizontal_interface[:, :, 1] * U_at_horizontal_interface[:, :, 1]
        )

    def at_current_time(self, tc):
        """
        Update the attributes at_vertical_interface and at_horizontal_interface of the class by updating the velocity field.

        - input:
            * tc: the current time
        """

        self.U.at_current_time(tc)
        self.diffusion_tensor_from_velocity_field()
