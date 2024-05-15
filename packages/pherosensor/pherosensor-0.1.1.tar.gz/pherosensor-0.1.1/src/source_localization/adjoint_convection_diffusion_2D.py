import os
import sys
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import cg
from scipy.sparse.linalg import gmres

from pheromone_dispersion.advection_operator import Advection
from pheromone_dispersion.advection_operator import AdvectionAdjoint
from pheromone_dispersion.diffusion_operator import Diffusion
from pheromone_dispersion.identity_operator import Id
from pheromone_dispersion.reaction_operator import Reaction


class AdjointDiffusionConvectionReaction2DEquation:
    """
    Class containing the adjoint model of the 2D diffusion-convection-reaction PDE model and its solvers
    """

    def __init__(self, U, K, coeff_depot, msh, time_discretization='semi-implicit', tol_inversion=1e-14):
        """
        Instanciation of the class.

        - input:
            * msh: object of the class mesh_rect_2D
            * U: object of the class velocity
            * K: object of the class diffusion_tensor
            * coeff_depot: array of shape (msh.y, msh.x) containing the deposition coefficient
            * obs: object of the class Obs, contains the observation operator and its derivative wrt the state variable
            * msh: object of the class mesh_rect_2D
            * time_discretization:
                string, describes the type of time discretization
                by default is 'semi-implicit', can also be 'implicit'
        - attributes:
            * msh: object of the class mesh_rect_2D
            * A: object of the class Advection, if the time discretization is semi-implicit, contains the convection linear operator
            * A_adjoint:
                object of the class Advection,
                if the time discretization is implicit, contains the adjoint of the convection linear operator
            * D: oject of the class Diffusion, contains the diffusion linear operator
            * R: object of the class Reaction, contains the reaction linear operator
            * ID: object of the class Id, contains the identity operator
            * obs: object of the class Obs, contains the observation operator and its derivative wrt the state variable
            * negative_divU_advection_term:
                object of the class Reaction,
                if the time discretization is semi-implicit, contains negative part of the reaction term in div U
                coming from the splitting of the adjoint of the advection term into a advection flux part and a reaction part
            * positive_divU_advection_term:
                object of the class Reaction,
                if the time discretization is semi-implicit, contains positive part of the reaction term in div U
                coming from the splitting of the adjoint of the advection term into a advection flux part and a reaction part
            * time_discretization: string, describes the type of time discretization
        """

        self.msh = msh
        self.D = Diffusion(K, msh)
        self.R = Reaction(coeff_depot, msh)
        self.Id = Id(msh)
        self.time_discretization = time_discretization
        implemented_solver_type = [
            'implicit',
            'semi-implicit',
            'implicit with matrix inversion',
            'semi-implicit with matrix inversion',
            'implicit with preconditionning',
            'implicit with stationnary matrix inversion',
        ]
        if self.time_discretization not in implemented_solver_type:
            raise ValueError("The given time discretization is not implemented.")

        if time_discretization == 'semi-implicit':
            self.A = Advection(U, msh)
            pos_div_val = np.where(self.A.U.div >= 0, self.A.U.div, 0.0)
            neg_div_val = np.where(self.A.U.div < 0, self.A.U.div, 0.0)
            self.negative_divU_advection_term = Reaction(neg_div_val, msh)
            self.positive_divU_advection_term = Reaction(pos_div_val, msh)

        self.A_adjoint = AdvectionAdjoint(U, msh)

        # elif time_discretization == 'implicit':
        #    self.A_adjoint = AdvectionAdjoint(U, msh)

        self.tol_inversion = tol_inversion
        self.transpose_inv_matrix_semi_implicit_scheme = None
        self.transpose_inv_matrix_implicit_scheme = None
        self.ILU_decomp_dic = {}
        self.jacobi = None
        self.inv_matrix_implicit_scheme_t_init = None

    def init_inverse_matrix(self, path_to_matrix=None, matrix_file_name=None):
        if path_to_matrix is None:
            path_to_matrix = './data'
        if not os.path.isdir(path_to_matrix):
            os.makedirs(path_to_matrix)
        if matrix_file_name is None:
            if self.time_discretization == 'semi-implicit with matrix inversion':
                matrix_file_name = 'inv_matrix_semi_implicit_scheme'
            if self.time_discretization == 'implicit with matrix inversion':
                matrix_file_name = 'inv_matrix_implicit_scheme'
            if self.time_discretization == 'implicit with stationnary matrix inversion':
                matrix_file_name = 'inv_matrix_implicit_scheme'
            matrix_file_name += '.npy'

        if not (Path(path_to_matrix) / matrix_file_name).exists():
            raise ValueError("The file to load does not exist. Either the path or the file name are wrong")

        else:
            print("=== Load of the inverse of the matrix of the implicit part of the " + self.time_discretization + " scheme ===")
            if self.time_discretization == 'semi-implicit with matrix inversion':
                self.transpose_inv_matrix_semi_implicit = np.transpose(np.load(Path(path_to_matrix) / matrix_file_name))
            if self.time_discretization == 'implicit with matrix inversion':
                self.transpose_inv_matrix_implicit_scheme = np.transpose(np.load(Path(path_to_matrix) / matrix_file_name))
            if self.time_discretization == 'implicit with stationnary matrix inversion':
                self.transpose_inv_matrix_implicit_scheme = np.transpose(np.load(Path(path_to_matrix) / matrix_file_name))

    def at_current_time(self, tc):
        """
        Update the linear operators of the PDE at a given time,
        i.e. update the attributes D and S of the class
        if the time discretization is semi-implicit, A, positive_divU_advection_term, negative_divU_advection_term,
        if the time discretization is implicit, A_adjoint,
        and the derivative of the observation operator of the attribute obs.

        - input:
            * tc: the current time
        """

        self.D.at_current_time(tc)

        if self.time_discretization == 'semi-implicit':
            self.A.at_current_time(tc, self.A.minus_U)
            pos_div_val = np.where(self.A.U.div >= 0, self.A.U.div, 0.0)
            neg_div_val = np.where(self.A.U.div < 0, self.A.U.div, 0.0)
            self.negative_divU_advection_term.update_reaction_coeff(neg_div_val)
            self.positive_divU_advection_term.update_reaction_coeff(pos_div_val)
        # elif self.time_discretization == 'implicit':
        self.A_adjoint.at_current_time(tc)

    def solver(self, adjoint_derivative_obs_operator, cost, display_flag=True):
        """
        solve the PDE on the whole time window

        - input:
            * cost:
                object of the class Cost, contains especially a method that compute the gradient of the objectif
                wrt the observed variable for the current optimization iteration and estimation of the observed variable
            * display_flag: boolean, True by default, print the evolution in time of the solver if True
        - output:
            * p:
                numpy array of shape (msh.t_array.size * msh.y.size * msh.x.size,),
                contains the adjoint state everywhere and at all time step concatenated in a vector
        """

        # initialization of the unknown variable at the final time and of the output
        p = np.zeros((self.msh.y.shape[0] * self.msh.x.shape[0],))
        p_out = np.array([])

        # loop until the initial time is reached (backward in time)
        for it, self.msh.t in enumerate(self.msh.t_array[::-1]):
            if display_flag:
                sys.stdout.write(f'\rt = {"{:.3f}".format(self.msh.t)} / {"{:.3f}".format(self.msh.T_final)} s')
                sys.stdout.flush()

            # update the coefficients of the equation at the current time and
            self.at_current_time(self.msh.t)

            # inverse the linear system using a conjugate gradient method for the current time step
            p_old = np.copy(p)  # NECESSARY???

            # inverse the linear system resulting the semi-implicit time discretization
            # using a conjugate gradient method for the current time step
            if self.time_discretization == 'semi-implicit':
                p, info = cg(
                    self.Id + self.msh.dt * (-self.D + self.R + self.negative_divU_advection_term),
                    p_old
                    - self.msh.dt
                    * (
                        self.A.rmatvec(p_old)
                        + self.positive_divU_advection_term(p_old)
                        + adjoint_derivative_obs_operator(self.msh.t, cost.gradient_objectif_wrt_d())
                    ),
                    x0=p_old,
                    tol=self.tol_inversion,
                )
                # p = self.transpose_inv_matrix_semi_implicit.dot(
                #     p_old
                #     - self.msh.dt
                #     * (-self.A_adjoint.matvec(p_old) + adjoint_derivative_obs_operator(self.msh.t, cost.gradient_objectif_wrt_d()))
                # )
            # inverse the linear system resulting the implicit time discretization using a gmres method for the current time step
            elif self.time_discretization == 'implicit':
                p, info = gmres(
                    self.Id + self.msh.dt * (-self.D + self.R + self.A_adjoint),
                    p_old - self.msh.dt * adjoint_derivative_obs_operator(self.msh.t, cost.gradient_objectif_wrt_d()),
                    x0=p_old,
                    tol=self.tol_inversion,
                )
            elif self.time_discretization == 'implicit with matrix inversion':
                p = self.transpose_inv_matrix_implicit_scheme[it, :, :].dot(
                    p_old - self.msh.dt * adjoint_derivative_obs_operator(self.msh.t, cost.gradient_objectif_wrt_d())
                )
                info = 0
            elif self.time_discretization == 'implicit with stationnary matrix inversion':
                RHS = p_old - self.msh.dt * adjoint_derivative_obs_operator(self.msh.t, cost.gradient_objectif_wrt_d())
                if not np.linalg.norm(RHS, ord=np.inf) < 1e-16:
                    LHS = (self.Id + self.msh.dt * (-self.D + self.R + self.A_adjoint)).matvec(p_old)
                    flag_residu = not np.linalg.norm(RHS - LHS) < self.tol_inversion * np.linalg.norm(RHS)
                    if flag_residu:
                        p = np.dot(self.transpose_inv_matrix_implicit_scheme, RHS)
                else:
                    p = np.zeros_like(p)
                info = 0

            if info > 0:
                raise ValueError(
                    "The algorithme used to solve the linear system has not converge"
                    + "to the expected tolerance or within the maximum number of iteration."
                )

            if info < 0:
                raise ValueError("The algorithme used to solve the linear system could not proceed du to illegal input or breakdown.")

            # store the result in the output variable
            p_out = np.append(np.copy(p), p_out)  # np.copy NECESSARY???

        return p_out
