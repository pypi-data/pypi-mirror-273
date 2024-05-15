import os
import sys
import time
from pathlib import Path

import numpy as np
import numpy.linalg as npl
import scipy.optimize as spo
from joblib import Parallel
from joblib import delayed

from source_localization.gradient_descent import gradient_descent
from source_localization.proximal_gradient import proximal_gradient


class Cost:
    """
    Class containing the cost function and its gradient
    """

    def __init__(self, msh, obs, ctrl, regularization_types=None, alpha=None, one_sensor_flag=False):
        """
        Instanciation of the class.

        - input:
            * msh: object of the class MeshRect2D
            * obs: object of the class Obs, contains the observations
            * ctrl: object of the class Control, contains the control, its background value and the covariance matrix
            * regularization_types:
                list of string, string or None,
                by default None, i.e. no regularization term is considered
                otherwise, contains the name of the type of regularization
            * alpha:
                dictionnary, float or None,
                weights coefficient of the regularization terms of the cost function
                by default None, i.e. no regularization term is considered
                otherwise, contains the type of regularization as keys
        - attributes:
            * msh: object of the class MeshRect2D
            * obs: object of the calss Obs, contains the observations
            * ctrl: object of the class Control, contains the control, its background value and the covariance matrix
            * regularization_types:
                list of string,
                by default an empty list, i.e. no regularization term is considered
                otherwise, contains the name of the type of regularization
            * alpha: float, weight coefficient between the observations term and the regularization term of the cost function
            * alpha:
                dictionnary,
                weights coefficient of the regularization terms of the cost function
                by default an empty dictionnary, i.e. no regularization term is considered
                otherwise, contains the type of regularization as keys and the related weight coefficient as value
            * j_obs: float, current value of the observations term of the cost function
            * j_reg:
                dictionnary,
                by default an empty dictionnary, i.e. no regularization term is considered
                otherwise, contains the type of regularization as keys
                and current value of the regularization terms of the cost function as value
        """

        self.obs = obs
        self.ctrl = ctrl
        self.msh = msh

        self.implemented_regularization_types = [
            'Tikhonov',
            'Population dynamic',
            'Stationnary population dynamic',
            'LASSO',
            'time group LASSO',
            'logarithm barrier',
        ]

        if regularization_types is None:
            self.regularization_types = []

        elif isinstance(regularization_types, str):
            self.regularization_types = [regularization_types]

        elif isinstance(regularization_types, list):
            self.regularization_types = regularization_types

        else:
            raise ValueError(
                "The given types of regularization term are neither None (no regularization term), nor a string or a list of string."
            )

        if not all(isinstance(regularization_type, str) for regularization_type in self.regularization_types):
            raise ValueError("One of the given types of regularization term is not a string.")

        for regularization_type in self.regularization_types:
            if regularization_type not in self.implemented_regularization_types:
                raise ValueError(
                    "The "
                    + regularization_type
                    + " regularization term has not been implemented."
                    + " It should be on of these: "
                    + ','.join(self.implemented_regularization_types)
                )

        if alpha is None:
            self.alpha = {}

        elif isinstance(alpha, float):
            if len(self.regularization_types) != 1:
                raise ValueError(
                    "The number of regularization terms in the list regularization_types is different "
                    + "than the number of weight coefficients in the dictionnary alpha."
                )
            else:
                self.alpha = {self.regularization_types[0]: alpha}

        elif isinstance(alpha, dict):
            self.alpha = alpha

        else:
            raise ValueError("The given weight coefficients are neither None (no regularization term), nor a float or a dictionnary.")

        if not len(list(self.alpha.keys())) == len(self.regularization_types):
            raise ValueError(
                "The number of regularization terms in the list regularization_types is different "
                + "than the number of weight coefficients in the dictionnary alpha."
            )

        keys_to_remove = []
        for key in self.alpha.keys():
            if key not in self.regularization_types:
                raise ValueError(
                    "The types of regularization term given in the list regularization_types are different"
                    + " than the types of regularization term given as key of the dictionnary alpha."
                    + " The "
                    + key
                    + "regularization term is found in the dictionnary alpha but not in the list regularization_types"
                )
            if not isinstance(self.alpha[key], float):
                raise ValueError("The weight coefficient related to the " + key + " regularization term is not a float.")

            if self.alpha[key] == 0.0:
                keys_to_remove.append(key)

        for key in keys_to_remove:
            del self.alpha[key]
            self.regularization_types.remove(key)
            print(
                "Warning: the regularization "
                + key
                + "has a weight coefficient equals to 0."
                + " Hence, this regularization term is not considered "
                + "and the key removed from the list regularization_types and the dictionary alpha."
            )

        self.j = 0
        self.j_obs = 0
        self.j_reg = {}
        for regularization_type in self.regularization_types:
            self.j_reg[regularization_type] = 0.0

        self.one_sensor_flag = one_sensor_flag
        if self.one_sensor_flag:
            self.onesensor_sum_p_over_ite = np.zeros((self.obs.nb_sensors, self.msh.t_array.size * self.msh.x.size * self.msh.y.size))
        else:
            self.onesensor_sum_p_over_ite = None

    def add_reg(self, regularization_type, alpha):
        """
        add a regularization term to the cost function

        - input:
            * regularization_type: string, contains the name of the type of regularization to add
            * alpha: float, associated weight coefficient
        - do:
            * chack that the type of regularization to add is implemented
            * update the attribute regularization_types by stacking regularization_type
            * update the attribute alpha by adding the key regularization_types and the associated value alpha
            * update the attribute j_reg by adding the key regularization_types and the initial value 0
        - TO DO:
            * add exceptions to make sure the input has a valid type
            * possibility to give a list of regularizations to add?
            * add case where regularization_type is already in regularizations_type
        """

        if regularization_type not in self.implemented_regularization_types:
            raise ValueError(
                "The "
                + regularization_type
                + " regularization term has not been implemented."
                + " It should be on of these: "
                + ','.join(self.implemented_regularization_types)
            )
        if alpha == 0:
            print(
                "Warning: the regularization term is to be added with a weight coefficient set to 0."
                + " Therefore, this regularization term is not considered and not added."
            )
        else:
            if regularization_type in self.regularization_types:
                print("Warning: the regularization term is already considered. The associated weight coefficient is still updated")
                self.modify_weight_reg(regularization_type, alpha)
            else:
                self.regularization_types.append(regularization_type)
                self.j_reg[regularization_type] = 0.0
                self.alpha[regularization_type] = alpha

    def modify_weight_reg(self, regularization_type, alpha):
        """
        add a regularization term to the cost function

        - input:
            * regularization_type: string, contains the name of the type of regularization to add
            * alpha: float, associated weight coefficient
        - do:
            * chack that the type of regularization to add is implemented
            * update the attribute regularization_types by stacking regularization_type
            * update the attribute alpha by adding the key regularization_types and the associated value alpha
            * update the attribute j_reg by adding the key regularization_types and the initial value 0
        - TO DO:
            * add exceptions to make sure the input has a valid type
            * possibility to give a list of regularizations to add?
        """

        if regularization_type not in self.implemented_regularization_types:
            raise ValueError(
                "The "
                + regularization_type
                + " regularization term has not been implemented."
                + " It should be on of these: "
                + ','.join(self.implemented_regularization_types)
            )
        if regularization_type not in self.regularization_types:
            raise ValueError(
                "The "
                + regularization_type
                + " regularization term is not considered up to now."
                + " These one are considered and therefore can be modified: "
                + ','.join(self.regularization_types)
            )
        self.alpha[regularization_type] = alpha
        if alpha == 0:
            print(
                "Warning: the weight coefficient associated to the regularization "
                + regularization_type
                + " is set to 0."
                + " Hence, this regularization term is not considered "
                + "and the key removed from the list regularization_types and the dictionary alpha."
            )
            self.remove_reg(regularization_type)

    def remove_reg(self, regularization_type):
        """
        remove a regularization term to the cost function

        - input:
            * regularization_type: string, contains the name of the type of regularization to add
        - do:
            * update the attribute regularization_types by removing regularization_type
            * update the attributes alpha and j_reg by deleting the key regularization_types
        - TO DO:
            * add exceptions to make sure the input has a valid type
            * possibility to give a list of regularizations to add?
        """

        if regularization_type not in self.implemented_regularization_types:
            raise ValueError(
                "The "
                + regularization_type
                + " regularization term has not been implemented."
                + " It should be on of these: "
                + ','.join(self.implemented_regularization_types)
            )
        if regularization_type not in self.regularization_types:
            print("Warning: the regularization " + regularization_type + "is not considered up to now. Thus, there is nothing to remove")
        else:
            self.regularization_types.remove(regularization_type)
            del self.j_reg[regularization_type]
            del self.alpha[regularization_type]

    def reg_cost(self):
        """
        Compute the regularization term of the cost function j_{reg}(S) = ||S-S^b||_{C^{-1}}

        - do:
            * evaluate the regularization term for the current value of the control
            * store the result in the attribute j_reg
        """

        if 'Tikhonov' in self.regularization_types:
            self.j_reg['Tikhonov'] = (
                self.alpha['Tikhonov']
                * self.msh.mass_cell
                * self.msh.dt
                * (self.ctrl.value - self.ctrl.background_value).dot(self.ctrl.C_inv.dot(self.ctrl.value - self.ctrl.background_value))
            )
        if 'Population dynamic' in self.regularization_types:
            self.j_reg['Population dynamic'] = (
                self.alpha['Population dynamic']
                * self.msh.mass_cell
                * self.msh.dt
                * npl.norm(self.ctrl.population_dynamic_model.matvec(self.ctrl.value)) ** 2
            )
        if 'Stationnary population dynamic' in self.regularization_types:
            self.j_reg['Stationnary population dynamic'] = (
                self.alpha['Stationnary population dynamic']
                * self.msh.mass_cell
                * self.msh.dt
                * npl.norm(self.ctrl.stationnary_population_dynamic_model.matvec(self.ctrl.value)) ** 2
            )
        if 'LASSO' in self.regularization_types:
            self.j_reg['LASSO'] = self.alpha['LASSO'] * self.msh.mass_cell * self.msh.dt * npl.norm(self.ctrl.value, 1)
        if 'time group LASSO' in self.regularization_types:
            self.j_reg['time group LASSO'] = (
                self.alpha['time group LASSO']
                * self.msh.mass_cell
                * np.sum(
                    np.array(
                        [
                            npl.norm(self.ctrl.value.reshape((self.msh.t_array.size, self.msh.y.size * self.msh.x.size))[:, i])
                            * np.sqrt(self.msh.dt)
                            for i in range(self.msh.y.size * self.msh.x.size)
                        ]
                    )
                )
            )
        if 'logarithm barrier' in self.regularization_types:
            self.j_reg['logarithm barrier'] = (
                self.alpha['logarithm barrier']
                * self.msh.mass_cell
                * self.msh.dt
                * np.sum(
                    -self.ctrl.log_barrier_threshold
                    * np.log(self.ctrl.log_barrier_threshold - self.ctrl.value[self.ctrl.exclusion_domain] ** 2)
                )
            )

    def obs_cost(self):
        """
        Compute the observation term of the cost function j_{obs}(d) = ||d-d^{obs}||_{R^{-1}}

        - do:
            * evaluate the observation term for the current estimate of the observed variable
            * store the result in the attribute j_obs
        """

        if np.array([np.isnan(self.obs.d_est[i]) for i in range(self.obs.N_obs)]).any():
            raise ValueError(
                "The vector of estimation of the observed variable has not been computed."
                + " The method observation operator should be used to computed this vector."
            )

        self.j_obs = (
            self.msh.mass_cell * self.msh.dt * (self.obs.d_est - self.obs.d_obs).dot(self.obs.R_inv.dot(self.obs.d_est - self.obs.d_obs))
        )

    def objectif(self):
        """
        Compute the objectif function J(S,d) = j_{obs}(d) + \alpha j_{reg}(S)
        the objectif function is defined such that the cost function satisfies j(S) = J(S, d(S))

        - do:
            * compute the regularization and observation term of the cost function
            * from the different terms, evaluate the cobjectif function
              for the current value of the control and the current estimate of the observed variable
            * store the result in the attribute j
        """

        self.obs_cost()
        self.reg_cost()
        self.j = self.j_obs
        for regularization_type in self.regularization_types:
            self.j += self.j_reg[regularization_type]

    def gradient_objectif_wrt_d(self):
        """
        Compute the gradient of the objectif function with respect to the estimate of the observed variable
        for the current estimate of the observed variable: \nabla_d J(d)= 2 R^{-1}(d-d^{obs})

        - output:
            * array of shape (N_obs, )
        """

        if np.array([np.isnan(self.obs.d_est[i]) for i in range(self.obs.N_obs)]).any():
            raise ValueError(
                "The vector of estimation of the observed variable has not been computed."
                + " The method observation operator should be used to computed this vector."
            )

        return 2 * self.obs.R_inv.dot(self.obs.d_est - self.obs.d_obs)

    def gradient_objectif_wrt_S(self):
        """
        Compute the gradient of the objectif function with respect to the control
        for the current value of the control: \nabla_S J(S)= 2 C^{-1}(S-S^b)

        - output:
            * array of shape (t.size * msh.x.size * msh.y.size, )
        """

        grad = np.zeros(
            self.msh.t_array.size * self.msh.x.size * self.msh.y.size,
        )
        if 'Tikhonov' in self.regularization_types:
            grad += self.alpha['Tikhonov'] * 2 * self.ctrl.C_inv.dot(self.ctrl.value - self.ctrl.background_value)
        if 'Population dynamic' in self.regularization_types:
            grad += (
                self.alpha['Population dynamic']
                * 2
                * self.ctrl.population_dynamic_model.rmatvec(self.ctrl.population_dynamic_model.matvec(self.ctrl.value))
            )
        if 'Stationnary population dynamic' in self.regularization_types:
            grad += (
                self.alpha['Stationnary population dynamic']
                * 2
                * self.ctrl.stationnary_population_dynamic_model.rmatvec(
                    self.ctrl.stationnary_population_dynamic_model.matvec(self.ctrl.value)
                )
            )
        if 'logarithm barrier' in self.regularization_types:
            grad += (
                self.alpha['logarithm barrier']
                * 2
                * self.ctrl.log_barrier_threshold
                * np.where(self.ctrl.exclusion_domain, 1, 0)
                / (self.ctrl.log_barrier_threshold - self.ctrl.value**2)
            )
        return grad

    def reg_proximal_operator(self, s, lam):
        """
        compute the proximal operator of the non-differentiable regularization terms
        for a given value of the control and of the parameter of the proximal operator

        - input:
            * s: array of shape (t.size * msh.x.size * msh.y.size, ), value of the control for which the proximal operator is estimated
            * lam: float, parameter of the proximal operator, coefficient of the soft-threshold in cas of a LASSO regularization
        - output:
            * prox: array of shape (t.size * msh.x.size * msh.y.size, ), estimation of the proximal operator
        - TO DO:
            * ajouter des exceptions pour assurer la taille en entrée?
            * vérifier la cohérence entre le prox de la norme 1 continue ?
        """

        if 'LASSO' in self.regularization_types:
            prox = np.array(
                [
                    np.multiply(np.sign(s[j]), np.max([abs(s[j]) - lam * self.alpha['LASSO'] * self.msh.mass_cell * self.msh.dt, 0]))
                    for j in range(s.size)
                ]
            )
            # prox = np.zeros((s.size,))
            # for j in range(s.size):
            #    prox[j] = np.multiply(np.sign(s[j]), np.max([abs(s[j]) - lam * self.alpha['LASSO'] * self.msh.mass_cell * self.msh.dt, 0]))

        elif 'time group LASSO' in self.regularization_types:
            s_reshape = s.reshape((self.msh.t_array.size, self.msh.y.size * self.msh.x.size))
            prox = np.array(
                [
                    s_reshape[:, i]
                    * np.maximum(
                        1 - lam * self.alpha['time group LASSO'] * self.msh.mass_cell / (npl.norm(s_reshape[:, i]) * np.sqrt(self.msh.dt)),
                        0,
                    )
                    for i in range(self.msh.y.size * self.msh.x.size)
                ]
            ).T.reshape((self.msh.t_array.size * self.msh.y.size * self.msh.x.size,))

        else:
            raise ValueError(
                "The proximal operator is not implemented for any of these regularization terms."
                + " If all the regularization terms are differentiable, there is no need of the proximal operator,"
                + " classical gradient descent algorithm should be used instead."
            )

        return prox

    def cost_and_gradient(self, S, direct_model, adjoint_model, sensor_importance=False, p_i_f='', display=False):
        """
        Compute the cost function j(S) and its gradient

        - input:
            * S: object of the class Source, contains the source term for which the cost and its gradient are evaluated
            * direct_model:
                object of the class DiffusionConvectionReaction2DEquation,
                contains the direct model used to compute the estimate of the observation variable
            * adjoint_model:
                object of the class AdjointDiffusionConvectionReaction2DEquation,
                contains the adjoint model associated to the direct model and used to compute the adjoint state
        - output:
            * j: the associated evaluation of the cost function
            * grad_j: the associated evaluation of the gradient of the cost function
        """

        # check that the setting of the attribute works

        # set the value of the control to the one provided as input
        self.ctrl.value = np.copy(S)  # NECESSARY???
        # set the value of the source term of the direct model to the value of the control
        self.ctrl.apply_control(direct_model)
        # solve the direct model with this value of the source term
        # and store the estimate of the state variable needed to compute the estimate of the observed variable
        if display:
            sys.stdout.write('\rrunning the direct model\n')
            sys.stdout.flush()
        direct_model.solver_est_at_obs_times(self.obs, display_flag=False)
        # compute the estimate of the observed variable
        if display:
            sys.stdout.write('\rrunning the observation operator\n')
            sys.stdout.flush()
        self.obs.obs_operator()

        # compute the adjoint state
        if display:
            sys.stdout.write('\rrunning the adjoint model\n')
            sys.stdout.flush()

        if not self.one_sensor_flag:
            p = adjoint_model.solver(self.obs.adjoint_derivative_obs_operator, self, display_flag=False)
        else:
            onesensor_p = self.calc_oncesensor_p(adjoint_model)
            p = np.sum(onesensor_p, axis=0)
            self.onesensor_sum_p_over_ite += onesensor_p

        # compute the cost function for the current value of the control
        self.objectif()

        # compute the gradient of the cost function for the current value of the control
        grad_j = self.gradient_objectif_wrt_S() - p

        return self.j, grad_j

    def calc_oncesensor_p(self, adjoint_model):
        """
        TO ADD
        """
        global number_of_sensor_done
        number_of_sensor_done = 0
        onesensor_p = np.zeros((self.obs.nb_sensors, self.msh.t_array.size * self.msh.x.size * self.msh.y.size))

        def process(i):
            # adj_der_obs_op = lambda t, dc: self.obs.onesensor_adjoint_derivative_obs_operator(t, dc, i)

            def adj_der_obs_op(t, dc):
                return self.obs.onesensor_adjoint_derivative_obs_operator(t, dc, i)

            global number_of_sensor_done
            number_of_sensor_done += 1
            onesensor_p[i, :] = adjoint_model.solver(adj_der_obs_op, self, display_flag=False)
            sys.stdout.write("mono-sensor adjoint model solved for %s sensors\n" % number_of_sensor_done)
            sys.stdout.flush()

        Parallel(n_jobs=self.obs.nb_sensors, prefer="threads", require='sharedmem')(delayed(process)(i) for i in range(self.obs.nb_sensors))
        return onesensor_p

    def minimize(
        self,
        direct_model,
        adjoint_model,
        method,
        j_obs_threshold=-np.inf,
        s_init=None,
        options={},
        path_save=None,
        restart_flag=False,
        sensor_importance=False,
    ):
        """
        Minimize the cost function

        - input:
            * direct_model:
                object of the class DiffusionConvectionReaction2DEquation,
                contains the direct model used to compute the estimate of the observation variable
            * adjoint_model:
                object of the class AdjointDiffusionConvectionReaction2DEquation,
                contains the adjoint model associated to the direct model and used to compute the adjoint state
            * method:
                string, describes the method used to minimize the cost function
                can be either 'gradient descent' or 'L-BFGS-B'
                for method='gradient descent', see the gradient descent method implemented below
                for method='L-BFGS-B', see the documentation of the minimize method of the package scipy.optimize
                (https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html)
            * options: dictionnary, contains the options to be given to the solver associated to the optimization method
        - output:
            * direct_model:
                object of the class DiffusionConvectionReaction2DEquation, contains the direct model with the optimal source term
            * j_obs:
                array of shape (N_ite, ), contains the observation term of the cost function at each iteration of the optimization process
            * j_reg:
                array of shape (N_ite, ),
                contains the regularization term of the cost function at each iteration of the optimization process
        """

        # set the iteration number, the outputs vector and the initial cost as global variable so they can be used in the callback function
        global iteration, j_obs, j_reg, j_0, t_i, traj_integrated_s, sum_step_size  # , S_vs_ite
        self.one_sensor_flag = sensor_importance

        if "step size" not in options.keys():
            options["step size"] = 1.0

        # initialize the iteration number and the outputs vector
        if not restart_flag:
            sys.stdout.write('initialization of the optimization process, computing the initial cost\n')
            sys.stdout.flush()
            # sys.stdout.write(f'\rinitialization of the optimization process, initially: j = {self.j} and j_obs = {self.j_obs}')
            # sys.stdout.flush()
            # compute the initial cost
            if s_init is None:
                self.ctrl.value = np.zeros(self.ctrl.value.shape)
            else:
                self.ctrl.value = s_init
            self.ctrl.apply_control(direct_model)
            direct_model.solver_est_at_obs_times(self.obs, display_flag=False)
            self.obs.obs_operator()
            self.objectif()
            j_0 = self.j
            iteration = 0
            nb_iteration_init = 0
            # S_vs_ite = []
            # d_est_vs_ite = []
            j_obs = []
            j_reg = {}
            traj_integrated_s = np.zeros_like(self.ctrl.value)
            sum_step_size = 0
            for regularization_type in self.regularization_types:
                j_reg[regularization_type] = []
            # f_old = np.inf
            if path_save is not None:
                # if the save directory does not exist, then it is created
                if not os.path.isdir(path_save):
                    os.makedirs(path_save)

        else:
            if not os.path.isdir(path_save):
                raise ValueError("The directory corresponding to the given path does not exist.")
            # if not ((Path(path_save) / 'S_vs_ite.npy').exists() and (Path(path_save) / 'j_obs_vs_ite.npy').exists()):
            if not ((Path(path_save) / 'j_obs_vs_ite.npy').exists()):
                raise ValueError("One of the files needed to restart the optimization processe does not exist in the the given directory.")
            # restart the optimization
            sys.stdout.write('restarting the optimization process from the data contained in the dir ' + str(path_save) + '\n')
            sys.stdout.flush()
            # S_optim = np.load(Path(path_save) / 'S_optim.npy')
            # S_vs_ite = list(np.load(Path(path_save) / 'S_vs_ite.npy'))
            # d_est_vs_ite = list(np.load(Path(path_save) / 'd_est_vs_ite.npy'))
            j_obs = np.load(Path(path_save) / 'j_obs_vs_ite.npy').tolist()
            iteration = len(j_obs)
            nb_iteration_init = len(j_obs)
            j_reg = {}
            j_0 = j_obs[0]
            if self.one_sensor_flag:
                self.onesensor_sum_p_over_ite = np.load(Path(path_save) / 'onesensor_sum_p_over_ite.npy')
                # if len(onesensor_p_vs_ite) != iteration:
                #     onesensor_p_vs_ite += [np.zeros(onesensor_p_vs_ite[0].shape) for i in range(iteration - len(onesensor_p_vs_ite))]
            for regularization_type in self.regularization_types:
                name = 'j_reg_' + regularization_type.replace(" ", "_") + '_vs_ite.npy'
                if not (Path(path_save) / ('j_reg_' + regularization_type.replace(" ", "_") + '_vs_ite.npy')).exists():
                    j_reg[regularization_type] = np.zeros((len(j_obs),)).tolist()
                    print(
                        "Warning: the regularization "
                        + regularization_type
                        + " term has not been found in the given directory."
                        + " It is assumed that this regularization term was not used previously and thus is set to 0."
                    )
                else:
                    j_reg[regularization_type] = np.load(Path(path_save) / name).tolist()
                    if len(j_reg[regularization_type]) != iteration:
                        j_reg[regularization_type] += [0 for i in range(iteration - len(j_reg[regularization_type]))]
                        print(
                            "Warning: the regularization "
                            + regularization_type
                            + " term was not computed at every iterations."
                            + " It is assumed that this regularization term was not used previously and thus is completed with 0."
                        )
                j_0 += j_reg[regularization_type][0]
            if not (Path(path_save) / ('traj_integrated_s.npy')).exists():
                traj_integrated_s = np.zeros_like(self.ctrl.value)
                print(
                    "Warning: trajectory integrated source term was not computed at every iterations."
                    + " It is set to 0 and previous iteration should e added later."
                )
            else:
                traj_integrated_s = np.load(Path(path_save) / 'traj_integrated_s.npy')
            if not (Path(path_save) / ('sum_step_size.npy')).exists():
                sum_step_size = 0
                print(
                    "Warning: the sum of the step size was not computed at every iterations."
                    + " It is set to 0 and previous iteration should e added later."
                )
            else:
                sum_step_size = np.load(Path(path_save) / 'sum_step_size.npy')
            self.ctrl.value = np.load(Path(path_save) / 'S_optim.npy')  # np.copy(S_vs_ite[-1])
            self.ctrl.apply_control(direct_model)
            # f_old = j_obs[-1] + j_reg[-1]
            # compute the initial cost
            direct_model.solver_est_at_obs_times(self.obs, display_flag=False)
            self.obs.obs_operator()
            self.objectif()

        def save_output():
            # difplay the results at the final iteration and the exit mesage of the optimization algorithm
            sys.stdout.write('\nfinal iteration:\n')
            sys.stdout.write(f'number of iteration = {iteration}\n')
            sys.stdout.write(f'j = {self.j/j_0} % of the initial cost\n')
            sys.stdout.write(f'j_obs = {self.j_obs/j_0} % of the initial cost\n')
            for key in self.j_reg.keys():
                sys.stdout.write(f'j_{key} = {self.j_reg[key]/j_0} % of the initial cost\n')
            # sys.stdout.write(f'the optimization exit successfully? {res.success}')
            # sys.stdout.write(res.message)
            sys.stdout.flush()
            if path_save is not None:
                # if the save directory does not exist, then it is created
                if not os.path.isdir(path_save):
                    os.makedirs(path_save)
                np.save(Path(path_save) / 'S_optim', self.ctrl.value)
                np.save(Path(path_save) / f'S_optim_ite_{"{0:04d}".format(iteration)}', self.ctrl.value)
                np.save(Path(path_save) / 'traj_integrated_s.npy', traj_integrated_s)
                np.save(Path(path_save) / f'traj_integrated_s_ite_{"{0:04d}".format(iteration)}.npy', traj_integrated_s)
                np.save(Path(path_save) / 'sum_step_size.npy', sum_step_size)
                np.save(Path(path_save) / f'sum_step_size_ite_{"{0:04d}".format(iteration)}.npy', sum_step_size)
                # np.save(Path(path_save) / 'S_vs_ite.npy', S_vs_ite)
                # np.save(Path(path_save) / 'd_est_vs_ite.npy', d_est_vs_ite)
                np.save(Path(path_save) / 'j_obs_vs_ite.npy', j_obs)
                for regularization_type in self.regularization_types:
                    name_alpha = 'alpha_' + regularization_type.replace(" ", "_") + '.npy'
                    name_j_reg = 'j_reg_' + regularization_type.replace(" ", "_") + '_vs_ite.npy'
                    np.save(Path(path_save) / name_alpha, self.alpha[regularization_type])
                    np.save(Path(path_save) / name_j_reg, j_reg[regularization_type])
                if "step size" in options.keys():
                    if not restart_flag:
                        step_size_array = []
                    else:
                        if (Path(path_save) / 'step_size_array.npy').exists():
                            step_size_array = np.load(Path(path_save) / 'step_size_array.npy').tolist()
                        else:
                            step_size_array = np.zeros((nb_iteration_init,)).tolist()
                step_size_array += [options["step size"] for i in range(iteration - nb_iteration_init)]
                np.save(Path(path_save) / 'step_size_array.npy', step_size_array)

        # define the callback function, update the iteration number and the outputs vector, and display the results at the current iteration
        def callback_fct(S):
            global iteration, t_i, traj_integrated_s, sum_step_size  # , S_vs_ite
            j_obs.append(self.j_obs)
            iteration += 1
            for regularization_type in self.regularization_types:
                j_reg[regularization_type].append(self.j_reg[regularization_type])
            if self.j_obs < j_obs_threshold:
                print('--- The cost of the observations is below the threshold. Thus, the optimization algorithm is terminated ---')
                save_output()
                sys.exit()
            sys.stdout.write(
                f'- \riteration {iteration}: j = {"{:.6e}".format(self.j)}'
                + f', j_obs = {"{:.6e}".format(self.j_obs)}'
                + f', ite comp time = {"{:.3e}".format(time.time()-t_i)}s -\n'
            )
            sys.stdout.flush()
            traj_integrated_s += options["step size"] * S
            sum_step_size += options["step size"]
            # S_vs_ite.append(np.copy(S))
            # d_est_vs_ite.append(np.copy(self.obs.d_est))
            # if iteration % 50 == 0 and iteration > 0 :
            #    #for regularization_type in self.regularization_types:
            #    #    name_alpha = 'alpha_' + regularization_type.replace(" ", "_") + '.npy'
            #    #    name_j_reg = 'j_reg_' + regularization_type.replace(" ", "_") + '_vs_ite.npy'
            #    #    np.save(Path(path_save) / name_alpha, self.alpha[regularization_type])
            #    #    np.save(Path(path_save) / name_j_reg, j_reg[regularization_type])
            #    #np.save(Path(path_save) / 'j_obs_vs_ite.npy', j_obs)
            #    np.save(Path(path_save) / f'S_vs_ite{"{0:04d}".format(iteration)}.npy', S_vs_ite)
            #    S_vs_ite = []
            #    #np.save(Path(path_save) / 'd_est_vs_ite.npy', d_est_vs_ite)
            # if sensor_importance:
            #    global onesensor_sum_p_over_ite
            #    # onesensor_p = self.calc_oncesensor_p(adjoint_model)
            #    onesensor_sum_p_over_ite += self.calc_oncesensor_p(adjoint_model)
            """sys.stdout.write(f'\riteration {iteration}:')
            sys.stdout.write(f'\rj = {self.j/j_0} % of the initial cost')
            sys.stdout.write(f'\rj_obs = {self.j_obs/j_0} % of the initial cost')
            sys.stdout.write(f'\rj_reg = {self.j_reg/j_0} % of the initial cost')"""
            t_i = time.time()

        t_i = time.time()
        # minimization using the L-BFGS-B method
        # this method is not efficient for now
        if method == 'L-BFGS-B':
            if 'LASSO' in self.regularization_types:
                raise ValueError(
                    "The cost function is not differentiable du to a LASSO regularization term"
                    "Hence, the L-BFGS-B algorithm can not be used." + " The proximal-gradient algorithm should be used instead."
                )
            sys.stdout.write('Optimizing using the L-BFGS-B algorithm \n')
            sys.stdout.flush()
            # initialize the bounds of control, we assume that the source term should be positive
            bounds = np.zeros((np.size(self.ctrl.value), 2))
            bounds[:, 1] = +np.inf
            # minimize the cost function using the L-BFGS-B algorithm implemented in the minimize method of the package scipy.optimize
            res = spo.minimize(
                self.cost_and_gradient,
                self.ctrl.value,
                args=(direct_model, adjoint_model),
                jac=True,
                method='L-BFGS-B',
                options=options,  # {"disp": True, "ftol": 1e-7, "gtol": 1e-6},
                callback=callback_fct,
                bounds=bounds,
            )
            s_a = np.copy(res.x)

        # minimization using the gradient descent method
        elif method == "gradient descent":
            if 'LASSO' in self.regularization_types or 'time group LASSO' in self.regularization_types:
                raise ValueError(
                    "The cost function is not differentiable du to a LASSO regularization term"
                    "Hence, the gradient descent algorithm can not be used." + " The proximal-gradient algorithm should be used instead."
                )
            sys.stdout.write('Optimizing using the gradient descent algorithm \n')
            sys.stdout.flush()
            s_a, _, _, _ = gradient_descent(
                self.cost_and_gradient,
                self.ctrl.value,
                args=(direct_model, adjoint_model),
                options=options,  # {"step size": 0.85, "ftol": 1e-7, "gtol": 1e-6},
                callback=callback_fct,
            )  # f_old = f_old

        # minimization using the gradient descent method
        elif method == "proximal gradient":
            if 'LASSO' not in self.regularization_types and 'time group LASSO' not in self.regularization_types:
                raise ValueError(
                    "The proximal operator is not implemented for any of these regularization terms"
                    + " or the weight coefficient of the LASSO regularization is 0."
                    + " If all the regularization terms are differentiable, the proximal gradient method is not appropriate."
                    + " Classical gradient descent algorithm should be used instead."
                )
            sys.stdout.write('Optimizing using the proximal gradient algorithm \n')
            sys.stdout.flush()
            s_a, _, _, _ = proximal_gradient(
                self.ctrl.value,
                self.cost_and_gradient,
                self.reg_proximal_operator,
                args=(direct_model, adjoint_model),
                options=options,
                callback=callback_fct,
            )

        else:
            raise ValueError("The given type of method has not been implemented.")

        # update the value of the control with its optimal value and apply it as souce term of the direct model
        self.ctrl.value = s_a
        self.ctrl.apply_control(direct_model)
        save_output()

        # if self.one_sensor_flag:
        #     return direct_model, j_obs, j_reg, s_a, onesensor_sum_p_over_ite
        # else:
        return direct_model, j_obs, j_reg, s_a
