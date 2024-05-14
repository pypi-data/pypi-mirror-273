import numpy as np
import scipy.sparse as sps

from source_localization.population_dynamique import PopulationDynamicModel
from source_localization.population_dynamique import StationnaryPopulationDynamicModel


class Control:
    """
    Class containing the control, its current and background value, and the background error covariance matrix
    """

    def __init__(self, background_source, msh, exclusion_domain=None, log_barrier_threshold=1e-10, population_dynamique_death_rate=None):
        """
        Instanciation of the class.

        - TO DO:
            * add exceptions in case the death rate is not defined
        - input:
            * background_source: object of the class Source, contains the background value of the source term
            * msh: object of the class MeshRect2D
        - attributes:
            * background_value:
                array of shape (t.size * msh.y.size * msh.x.size,),
                contains the background value of the source term
                the background values of control each time step of the direct model are concatenated
            * value:
                array of shape (t.size * msh.y.size * msh.x.size,),
                contains the current value of the control and is initialized with the background value
            * C_inv:
                array of shape (t.size * msh.y.size * msh.x.size, t.size * msh.y.size * msh.x.size),
                contains inverse of the background error covariance matrix, by default the identity
        """
        if msh.t_array is None:
            raise ValueError(
                "The array containing the time at which the direct model is solved, has not been correctly initialized."
                + " This is probably because the time step has not been computed so the CFL condition is satisfied."
                + " The method calc_CFL of the class MeshRect2D should then be executed first."
            )

        background_value = np.array([])
        for it, t in enumerate(msh.t_array):
            background_source.at_current_time(t)
            value_prov = np.copy(background_source.value)  # NECESSARY???
            background_value = np.append(background_value, value_prov.ravel())
        self.background_value = np.copy(background_value)
        self.value = np.zeros(background_value.shape)
        self.C_inv = sps.identity(np.size(background_value), dtype=int)
        # self.population_dynamic_model = PopulationDynamicModel(msh)
        self.population_dynamic_model = PopulationDynamicModel(msh, death_rate=population_dynamique_death_rate)
        self.stationnary_population_dynamic_model = StationnaryPopulationDynamicModel(msh)

        # RAJOUTER DES TESTS SUR LES PARAMETRES DE LA LOG BARRIER
        if exclusion_domain is None:
            self.exclusion_domain = []
        else:
            self.exclusion_domain = exclusion_domain
        self.log_barrier_threshold = log_barrier_threshold

    def apply_control(self, direct_model):
        """
        apply the current value of the control to an direct model

        - input:
            * direct_model: object of the class DiffusionConvectionReaction2DEquation, contains the direct model
        - do:
            * set the source terme of direct_model as the current value of the control
        """

        value_prov = np.copy(self.value)  # NECESSARY???
        direct_model.set_source(
            value_prov.reshape((direct_model.msh.t_array.shape[0], direct_model.msh.y.shape[0], direct_model.msh.x.shape[0])),
            t=direct_model.msh.t_array,
        )

    def set_C_inv_to_id_on_initial_time(self, msh):
        array = np.zeros((msh.t_array.size, msh.y.size, msh.x.size))
        array[0, :, :] = 1
        diag = array.reshape((msh.t_array.size * msh.y.size * msh.x.size))
        self.C_inv = sps.diags(diag)
