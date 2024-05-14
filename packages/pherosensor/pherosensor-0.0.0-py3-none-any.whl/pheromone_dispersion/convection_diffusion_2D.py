import os
import sys
import time
from pathlib import Path

import numpy as np
import scipy as sp
from scipy.sparse.linalg import cg
from scipy.sparse.linalg import gmres
from scipy.sparse.linalg import spsolve_triangular

from pheromone_dispersion.advection_operator import Advection
from pheromone_dispersion.diffusion_operator import Diffusion
from pheromone_dispersion.identity_operator import Id
from pheromone_dispersion.reaction_operator import Reaction
from pheromone_dispersion.source_term import Source

"""
Ajouter des tests dans le cas stationnaire pour verifier que les matrices sont 3D
"""


class DiffusionConvectionReaction2DEquation:
    """
    Class containing the 2D diffusion-convection-reaction PDE and its solvers
    """

    def __init__(self, U, K, coeff_depot, S, msh, time_discretization='semi-implicit', tol_inversion=1e-14):
        """
        Instanciation of the class.

        - input:
            * msh: object of the class MeshRect2D
            * U: object of the class Velocity
            * K: object of the class DiffusionTensor
            * coeff_depot: array of shape (msh.y, msh.x) containing the deposition coefficient
            * S: object of the class Source, contains the source term
            * time_discretization:
                string, describes the type of time discretization
                by default is 'semi-implicit', can also be 'implicit'
        - attributes:
            * msh: object of the class MeshRect2D
            * A: object of the class Advection, contains the convection linear operator
            * D: oject of the class Diffusion, contains the diffusion linear operator
            * R: object of the class Reaction, contains the reaction linear operator
            * ID: object of the class Id, contains the identity operator
            * S: object of the class Source, contains the source term
            * time_discretization: string, describes the type of time discretization
        - TO DO:
            * Add exceptions in case the matrix are computed/initialized
        """

        self.msh = msh
        self.A = Advection(U, msh)
        self.D = Diffusion(K, msh)
        self.R = Reaction(coeff_depot, msh)
        self.Id = Id(msh)
        self.S = S
        self.time_discretization = time_discretization
        self.tol_inversion = tol_inversion
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
        self.inv_matrix_semi_implicit_scheme = None
        self.inv_matrix_implicit_scheme = None
        self.ILU_decomp_dic = {}
        self.jacobi = None
        self.inv_matrix_implicit_scheme_t_init = None

    def spsolve_lu(self, b):
        if self.ILU_decomp_dic['perm r'] is not None:
            b_old = b.copy()
            for old_ndx, new_ndx in enumerate(self.ILU_decomp_dic['perm r']):
                b[new_ndx] = b_old[old_ndx]
        try:  # unit_diagonal is a new kw
            c = spsolve_triangular(self.ILU_decomp_dic['L'], b, lower=True, unit_diagonal=True)
        except TypeError:
            c = spsolve_triangular(self.ILU_decomp_dic['L'], b, lower=True)
        px = spsolve_triangular(self.ILU_decomp_dic['U'], c, lower=False)
        if self.ILU_decomp_dic['perm c'] is None:
            return px
        return px[self.ILU_decomp_dic['perm c']]

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
            print("=== Computation of the inverse of the matrix of the implicit part of the " + self.time_discretization + " scheme ===")
            Identity = np.identity(self.msh.y.size * self.msh.x.size)

            if self.time_discretization == 'semi-implicit with matrix inversion':
                matrix_semi_implicit_scheme = Identity + self.msh.dt * (-self.D._matmat(Identity) + self.R._matmat(Identity))
                self.inv_matrix_semi_implicit_scheme = sp.linalg.inv(matrix_semi_implicit_scheme)
                np.save(Path(path_to_matrix) / matrix_file_name + '.npy', self.inv_matrix_semi_implicit_scheme)

            if self.time_discretization == 'implicit with matrix inversion':
                t_i = time.time()
                for it, self.msh.t in enumerate(self.msh.t_array[1:]):
                    self.at_current_time(self.msh.t)
                    matrix_implicit_scheme = Identity + self.msh.dt * (
                        -self.D._matmat(Identity) + self.R._matmat(Identity) + self.A._matmat(Identity)
                    )
                    self.inv_matrix_implicit_scheme = sp.linalg.inv(matrix_implicit_scheme)
                    print("--- Computation at time t= ", self.msh.t, "in ", time.time() - t_i, " s")
                    t_i = time.time()
                    np.save(
                        Path(path_to_matrix) / matrix_file_name + f'_ite{"{0:04d}".format(it+1)}' + '.npy', self.inv_matrix_implicit_scheme
                    )

            if self.time_discretization == 'implicit with stationnary matrix inversion':
                t_i = time.time()
                matrix_implicit_scheme = Identity + self.msh.dt * (
                    -self.D._matmat(Identity) + self.R._matmat(Identity) + self.A._matmat(Identity)
                )
                self.inv_matrix_implicit_scheme = sp.linalg.inv(matrix_implicit_scheme)
                print("--- Computation at time t= ", self.msh.t, "in ", time.time() - t_i, " s")
                t_i = time.time()
                np.save(Path(path_to_matrix) / matrix_file_name + '.npy', self.inv_matrix_implicit_scheme)

        else:
            print("=== Load of the inverse of the matrix of the implicit part of the " + self.time_discretization + " scheme ===")
            if self.time_discretization == 'semi-implicit with matrix inversion':
                self.inv_matrix_semi_implicit_scheme = np.load(Path(path_to_matrix) / matrix_file_name)
            if self.time_discretization == 'implicit with matrix inversion':
                self.inv_matrix_implicit_scheme = np.load(Path(path_to_matrix) / matrix_file_name)
            if self.time_discretization == 'implicit with stationnary matrix inversion':
                self.inv_matrix_implicit_scheme = np.load(Path(path_to_matrix) / matrix_file_name)
            if self.time_discretization == 'implicit with preconditionning':
                self.inv_matrix_implicit_scheme_t_init = np.load(Path(path_to_matrix) / matrix_file_name)

    def set_source(self, value, t=None):
        """
        Update the source term with the values provided as input

        - input:
            * value: numpy array of shape (t.size, msh.y.size, msh.x.size), the new values of the source term
            * t: numpy array of shape (t.size,), the vector containing the associated times, by default None if the source is stationnary
        """
        setattr(self, 'S', Source(self.msh, value, t=t))

    def at_current_time(self, tc, i=None):
        """
        Update the linear operators of the PDE (attributes A, D and S of the class) at a given time.

        - input:
            * tc: the current time
        """
        self.S.at_current_time(tc)

        if not self.time_discretization == 'implicit with stationnary matrix inversion':
            self.A.at_current_time(tc, self.A.U)
            self.D.at_current_time(tc)

        # if self.time_discretization ==  'implicit with preconditionning':
        #    #dic_name = 'ILU_decomp_dic'
        #    path = './output'
        #    matrix_name = 'Jacobi_matrix'
        #    matrix_file_name = matrix_name + f'_ite{"{0:04d}".format(i+1)}.npz'
        #    self.jacobi = sps.load_npz(Path(path) / matrix_file_name)

        # dic_file_name = dic_name + f'_ite{"{0:04d}".format(i+1)}.pklz'
        # with gzip.open(Path(path) / dic_file_name, 'rb') as f:
        #    self.ILU_decomp_dic = pickle.load(f)

    def solver_one_time_step(self, c):
        """
        solve the PDE for one time step
        inverse the linear system (I + dt (- D + R)).c^{n+1} = c^n + dt (- A.c^n + S)

        - input:
            * c: numpy array of shape (msh.y.size, msh.x.size), contains the concentration of pheromones at the previous time step
        - output:
            * numpy array of shape (msh.y.size, msh.x.size), resulting concentration at the current time step
        """

        if c.shape != (self.msh.y.size, self.msh.x.size):
            raise ValueError(
                "The shape of the concentration at the previous time at the center of the cells does not match with the shape of the msh."
            )

        # ravel the matrix of concentration into a msh.y.size*msh.x.size size vector to match with the format of the LinearOperator class
        c_ravel = c.ravel()

        # inverse the linear system using a conjugate gradient method
        c_ravel, tol = cg(self.Id + self.msh.dt * (-self.D + self.R), c_ravel + self.msh.dt * (-self.A.dot(c_ravel) + self.S.value.ravel()))
        return c_ravel.reshape((c.shape))

    def solver(self, save_all=False, path_save='./save/', display_flag=True):
        """
        solve the PDE on the whole time window

        - input:
            * save_all:
                boolean, False by default,
                the matrix of the concentration at every time step and the vector of time are saved in numpy arrays if True
            * path_save: string, './save/' by default, contains the path of the directory in which the ouputs are saved
            * display_flag: boolean, True by default, print the evolution in time of the solver if True
        - output:
            * c: numpy array of shape (msh.t_array.size, msh.y.size, msh.x.size), contains the concentration at all time steps
        """

        # initialization of the unknown variable at the current time
        c = np.zeros((self.msh.y.shape[0] * self.msh.x.shape[0],))

        # initialization of the outputs array to be saved
        if save_all:
            # if the save directory does not exist, then it is created
            if not os.path.isdir(path_save):
                os.makedirs(path_save)
        c_save = np.zeros((self.msh.t_array.shape[0], self.msh.y.shape[0], self.msh.x.shape[0]))

        # loop until the final time or the steady state is reached
        for it, self.msh.t in enumerate(self.msh.t_array[1:]):
            if display_flag:
                sys.stdout.write(f'\rt = {"{:.3f}".format(self.msh.t)} / {"{:.3f}".format(self.msh.T_final)} s')
                sys.stdout.flush()

            # update the coefficients of the equation at the current time and
            self.at_current_time(self.msh.t, i=it)
            # store the concentration at the previous time step
            c_old = np.copy(c)  # NECESSARY???

            # inverse the linear system resulting the semi-implicit time discretization
            # using a conjugate gradient method for the current time step
            if self.time_discretization == 'semi-implicit with matrix inversion':
                c = self.inv_matrix_semi_implicit_scheme.dot(c_old + self.msh.dt * (-self.A.matvec(c_old) + self.S.value.ravel()))
                info = 0
            elif self.time_discretization == 'semi-implicit':
                c, info = cg(
                    self.Id + self.msh.dt * (-self.D + self.R),
                    c_old + self.msh.dt * (-self.A.matvec(c_old) + self.S.value.ravel()),
                    x0=c_old,
                    tol=self.tol_inversion,
                )
            # inverse the linear system resulting the implicit time discretization using a gmres method for the current time step
            elif self.time_discretization == 'implicit':
                c, info = gmres(
                    self.Id + self.msh.dt * (-self.D + self.R + self.A),
                    c_old + self.msh.dt * self.S.value.ravel(),
                    x0=c_old,
                    tol=self.tol_inversion,
                )
            elif self.time_discretization == 'implicit with preconditionning':
                precond = (
                    self.inv_matrix_implicit_scheme_t_init
                    # self.jacobi
                    # spsl.LinearOperator((self.msh.x.size*self.msh.y.size,self.msh.x.size*self.msh.y.size),matvec=self.spsolve_lu)
                )
                c, info = gmres(
                    self.Id + self.msh.dt * (-self.D + self.R + self.A),
                    c_old + self.msh.dt * self.S.value.ravel(),
                    x0=c_old,
                    tol=self.tol_inversion,
                    M=precond,
                )
            elif self.time_discretization == 'implicit with matrix inversion':
                c = self.inv_matrix_implicit_scheme[it, :, :].dot(c_old + self.msh.dt * self.S.value.ravel())
                info = 0
            elif self.time_discretization == 'implicit with stationnary matrix inversion':
                RHS = c_old + self.msh.dt * self.S.value.ravel()
                LHS = (self.Id + self.msh.dt * (-self.D + self.R + self.A)).matvec(c_old)
                flag_residu = not np.linalg.norm(RHS - LHS) < self.tol_inversion * np.linalg.norm(RHS)
                if flag_residu:
                    c = np.dot(self.inv_matrix_implicit_scheme, RHS)
                info = 0

            if info > 0:
                raise ValueError(
                    "The algorithme used to solve the linear system has not converge"
                    + "to the expected tolerance or within the maximum number of iteration."
                )

            if info < 0:
                raise ValueError("The algorithme used to solve the linear system could not proceed du to illegal input or breakdown.")

            c_save[it + 1, :, :] = c.reshape((self.msh.y.shape[0], self.msh.x.shape[0]))

        # save the ouputs
        if save_all:
            if not os.path.isdir(Path(path_save)):
                os.makedirs(Path(path_save))
            np.save(Path(path_save) / 'c.npy', c_save)

        return c_save

    def solver_save_all(self, path_save='./save/', display_flag=True, save_rate=1000):
        """
        solve the PDE on the whole time window

        - input:
            * save_all:
                boolean, False by default,
                the matrix of the concentration at every time step and the vector of time are saved in numpy arrays if True
            * path_save: string, './save/' by default, contains the path of the directory in which the ouputs are saved
            * display_flag: boolean, True by default, print the evolution in time of the solver if True
        - output:
            * c: numpy array of shape (msh.t_array.size, msh.y.size, msh.x.size), contains the concentration at all time steps
        """

        # initialization of the unknown variable at the current time
        c = np.zeros((self.msh.y.shape[0] * self.msh.x.shape[0],))

        t_save = []
        c_save = []  # np.zeros((, self.msh.y.shape[0] * self.msh.x.shape[0],))

        # initialization of the outputs array to be saved
        # if the save directory does not exist, then it is created
        if not os.path.isdir(path_save):
            os.makedirs(path_save)

        # loop until the final time or the steady state is reached
        for it, self.msh.t in enumerate(self.msh.t_array[1:]):
            if display_flag:
                # print(f"\rt = {"{:.3f}".format(self.msh.t)} / {"{:.3f}".format(self.msh.T_final)} s")
                sys.stdout.write(f'\n\rt = {"{:.3f}".format(self.msh.t)} / {"{:.3f}".format(self.msh.T_final)} s')
                sys.stdout.flush()

            # update the coefficients of the equation at the current time and
            self.at_current_time(self.msh.t, i=it)
            # store the concentration at the previous time step
            c_old = np.copy(c)  # NECESSARY???

            # inverse the linear system resulting the semi-implicit time discretization
            # using a conjugate gradient method for the current time step
            if self.time_discretization == 'semi-implicit with matrix inversion':
                c = self.inv_matrix_semi_implicit_scheme.dot(c_old + self.msh.dt * (-self.A.matvec(c_old) + self.S.value.ravel()))
                info = 0
            elif self.time_discretization == 'semi-implicit':
                c, info = cg(
                    self.Id + self.msh.dt * (-self.D + self.R),
                    c_old + self.msh.dt * (-self.A.matvec(c_old) + self.S.value.ravel()),
                    x0=c_old,
                    tol=self.tol_inversion,
                )
            # inverse the linear system resulting the implicit time discretization using a gmres method for the current time step
            elif self.time_discretization == 'implicit':
                c, info = gmres(
                    self.Id + self.msh.dt * (-self.D + self.R + self.A),
                    c_old + self.msh.dt * self.S.value.ravel(),
                    x0=c_old,
                    tol=self.tol_inversion,
                )
            elif self.time_discretization == 'implicit with preconditionning':
                precond = (
                    self.inv_matrix_implicit_scheme_t_init
                    # self.jacobi
                    # spsl.LinearOperator((self.msh.x.size*self.msh.y.size,self.msh.x.size*self.msh.y.size),matvec=self.spsolve_lu)
                )
                c, info = gmres(
                    self.Id + self.msh.dt * (-self.D + self.R + self.A),
                    c_old + self.msh.dt * self.S.value.ravel(),
                    x0=c_old,
                    tol=self.tol_inversion,
                    M=precond,
                )
            elif self.time_discretization == 'implicit with matrix inversion':
                c = self.inv_matrix_implicit_scheme[it, :, :].dot(c_old + self.msh.dt * self.S.value.ravel())
                info = 0
            elif self.time_discretization == 'implicit with stationnary matrix inversion':
                RHS = c_old + self.msh.dt * self.S.value.ravel()
                LHS = (self.Id + self.msh.dt * (-self.D + self.R + self.A)).matvec(c_old)
                flag_residu = not np.linalg.norm(RHS - LHS) < self.tol_inversion * np.linalg.norm(RHS)
                if flag_residu:
                    c = np.dot(self.inv_matrix_implicit_scheme, RHS)
                # c = np.dot(self.inv_matrix_implicit_scheme, c_old + self.msh.dt * self.S.value.ravel())
                info = 0

            if info > 0:
                raise ValueError(
                    "The algorithme used to solve the linear system has not converge"
                    + "to the expected tolerance or within the maximum number of iteration."
                )

            if info < 0:
                raise ValueError("The algorithme used to solve the linear system could not proceed du to illegal input or breakdown.")
            if it % save_rate == 0:
                t_save.append(self.msh.t)
                c_save.append(c.reshape((self.msh.y.shape[0], self.msh.x.shape[0])))

        np.save(Path(path_save) / 'c_save.npy', c_save)
        np.save(Path(path_save) / 't_save.npy', t_save)

    def solver_est_at_obs_times(self, obs, display_flag=True):
        """
        solve the PDE on the whole time window and store the resulting estimations of the concentration at the observations times

        - TO DO:
            * check that the function works
        - input:
            * obs:
                object of the class Obs, contains the observations and the observations times at which we aim to estimate the concentration
        - do:
            * solve the PDE on the whole time window
              but only store the resulting estimations at the observations times in the atrtibutes c_est of obs
        """

        # initialization of the unknown variable at the current time
        c = np.zeros((self.msh.y.shape[0] * self.msh.x.shape[0],))

        if 0 in obs.index_obs_to_index_time_est:
            c_prov = c.reshape((self.msh.y.shape[0], self.msh.x.shape[0]))
            for index_obs in obs.index_time_est_to_index_obs[0]:
                index_x_est = np.argmin(np.abs(self.msh.x - obs.X_obs[index_obs, 0]))
                index_y_est = np.argmin(np.abs(self.msh.y - obs.X_obs[index_obs, 1]))
                obs.c_est[index_obs] = c_prov[index_y_est, index_x_est]

        # loop until the final time or the steady state is reached
        for it, self.msh.t in enumerate(self.msh.t_array[1:]):
            if display_flag:
                sys.stdout.write(f'\rt = {"{:.3f}".format(self.msh.t)} / {"{:.3f}".format(self.msh.T_final)} s')
                sys.stdout.flush()
            # update the coefficients of the equation at the current time and
            self.at_current_time(self.msh.t, i=it)
            # store the concentration at the previous time step
            c_old = np.copy(c)  # NECESSARY???

            # inverse the linear system resulting the semi-implicit time discretization
            # using a conjugate gradient method for the current time step
            if self.time_discretization == 'semi-implicit with matrix inversion':
                c = self.inv_matrix_semi_implicit_scheme.dot(c_old + self.msh.dt * (-self.A.matvec(c_old) + self.S.value.ravel()))
                info = 0
            elif self.time_discretization == 'semi-implicit':
                c, info = cg(
                    self.Id + self.msh.dt * (-self.D + self.R),
                    c_old + self.msh.dt * (-self.A.matvec(c_old) + self.S.value.ravel()),
                    x0=c_old,
                    tol=self.tol_inversion,
                )
            # inverse the linear system resulting the implicit time discretization using a gmres method for the current time step
            elif self.time_discretization == 'implicit':
                c, info = gmres(
                    self.Id + self.msh.dt * (-self.D + self.R + self.A),
                    c_old + self.msh.dt * self.S.value.ravel(),
                    x0=c_old,
                    tol=self.tol_inversion,
                )
            elif self.time_discretization == 'implicit with matrix inversion':
                c = self.inv_matrix_implicit_scheme[it, :, :].dot(c_old + self.msh.dt * self.S.value.ravel())
                info = 0
            elif self.time_discretization == 'implicit with stationnary matrix inversion':
                RHS = c_old + self.msh.dt * self.S.value.ravel()
                if not np.linalg.norm(RHS, ord=np.inf) < 1e-16:
                    LHS = (self.Id + self.msh.dt * (-self.D + self.R + self.A)).matvec(c_old)
                    flag_residu = not np.linalg.norm(RHS - LHS) < self.tol_inversion * np.linalg.norm(RHS)
                    # print(np.linalg.norm(RHS),np.linalg.norm(RHS, ord=np.inf))
                    if flag_residu:
                        c = np.dot(self.inv_matrix_implicit_scheme, RHS)
                else:
                    c = np.zeros_like(c)  # print("the norm is 0")
                # c = np.dot(self.inv_matrix_implicit_scheme, c_old + self.msh.dt * self.S.value.ravel())
                info = 0

            if info > 0:
                raise ValueError(
                    "The algorithme used to solve the linear system has not converge"
                    + "to the expected tolerance or within the maximum number of iteration."
                )

            if info < 0:
                raise ValueError("The algorithme used to solve the linear system could not proceed du to illegal input or breakdown.")

            it += 1
            if it in obs.index_obs_to_index_time_est:
                c_prov = c.reshape((self.msh.y.shape[0], self.msh.x.shape[0]))
                for index_obs in obs.index_time_est_to_index_obs[it]:
                    i = np.where(obs.index_obs_to_index_time_est[index_obs, :] == it)
                    index_x_est = np.argmin(np.abs(self.msh.x - obs.X_obs[index_obs, 0]))
                    index_y_est = np.argmin(np.abs(self.msh.y - obs.X_obs[index_obs, 1]))
                    obs.c_est[index_obs, i] = c_prov[index_y_est, index_x_est]

    def solver_steady_state(self):
        """
        solve the steady-state version of the PDE
        inverse the linear system (- D + A + R) c = S using a conjugate gradient method

        - output:
            * numpy array of shape (msh.y.size, msh.x.size), resulting concentration at the steady state
        """

        c_ravel, tol = cg(-self.D + self.A + self.R, self.S.value.ravel())
        return c_ravel.reshape((self.msh.y.shape[0], self.msh.x.shape[0]))
