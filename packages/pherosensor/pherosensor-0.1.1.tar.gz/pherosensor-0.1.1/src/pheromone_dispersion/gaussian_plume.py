import matplotlib.pyplot as plt
import numpy as np
import scipy.special as sps


class Gaussian_plume_1source:
    def __init__(self, Xs, K, u, Q, w_set, w_dep):
        # location and emission rate of the source
        self.xs = Xs[0]
        self.ys = Xs[1]
        self.zs = Xs[2]
        self.Q = Q

        # parameter of the equation, resp. the diffusion coefficient, the wind velocity
        self.K = K
        self.u = u

        # parameter of the settling and deposition of pheromones
        self.w_set = w_set
        self.w_dep = w_dep

    def CDV(self, x):
        # CDV for a constant K and u
        return self.K * x / self.u

    def gaussian_plume(self, xx, yy, zz):
        x = xx - self.xs
        y = yy - self.ys
        z = zz - self.zs

        r = self.CDV(x)
        w_o = self.w_dep - 0.5 * self.w_set

        a = np.exp(-0.25 * y**2 / r) / np.sqrt(4 * np.pi * r)
        b = np.exp(-0.25 * (zz - self.zs) ** 2 / r) + np.exp(-0.25 * (zz + self.zs) ** 2 / r)
        b -= (
            2
            * w_o
            * np.sqrt(np.pi * r)
            * np.exp((w_o * (z + 2 * self.zs) / self.K) + (w_o**2 * r / self.K**2))
            * sps.erfc(0.5 * (z + 2 * self.zs) / np.sqrt(r) + w_o * np.sqrt(r) / self.K)
            / self.K
        )
        b /= np.sqrt(4 * np.pi * r)
        sep_var = np.exp(-(0.5 * self.w_set * z / self.K) - (0.25 * self.w_set**2 * r / self.K**2))

        return np.where(r <= 0, 0, self.Q * a * b * sep_var / self.u)


class Gaussian_plume_multisources:
    def __init__(self, Xs, K, u, Q, w_set, w_dep):
        # location and emission rate of the source
        self.n_source = np.size(Q)
        self.gps_1s = [Gaussian_plume_1source(Xs[i], K, u, Q[i], w_set, w_dep) for i in range(self.n_source)]
        # vérifier la consistance des axes et des indices avec le solver de convection diffusion

    def gaussian_plume(self, xx, yy, zz):
        return np.sum([self.gps_1s[i].gaussian_plume(xx, yy, zz) for i in range(self.n_source)], axis=0)


def plot_verticalxs(xv, yv, zv, yp, C):
    i_y = np.argmin(np.abs(yv[0, :, 0] - yp))
    n_c = np.shape(C)[0]
    cmax = 0
    for i in range(n_c):  # a essayer de condenser en une ligne
        ci = C[i]
        cmax = max((cmax, np.nanmax(ci[:, int(i_y)])))
    for i in range(n_c):
        ci = C[i]
        plt.figure(i)
        plt.pcolormesh(xv[:, 0, 0], zv[0, 0, :], ci[:, i_y, :].T, cmap='jet', vmin=0.0, vmax=cmax)
        plt.xlabel('$x$ ($m$)')
        plt.ylabel('$z$ ($m$)')
        cbar = plt.colorbar()
        cbar.set_label('$C$ ($g.m^{-3}$)', rotation=270)
    plt.show()


def plot_horizontalxs(xv, yv, zv, zp, C):
    i_z = np.argmin(np.abs(zv - zp))
    n_c = np.shape(C)[0]
    cmax = 0
    for i in range(n_c):  # a essayer de condenser en une ligne
        ci = C[i]
        cmax = max((cmax, np.nanmax(ci[:, :, int(i_z)])))
    for i in range(n_c):
        ci = C[i]
        plt.figure(i)
        plt.pcolormesh(xv, yv, ci[:, :, i_z].T, cmap='jet', vmin=0.0, vmax=cmax)  # , norm=norm)
        plt.xlabel('$x$ ($m$)')
        plt.ylabel('$y$ ($m$)')
        cbar = plt.colorbar()
        cbar.set_label('$C$ ($g.m^{-3}$)', rotation=270)
    plt.show()


def plot_downwindprofile(xv, yv, zv, yp, zp, C, xmax=None, Cmax=None):
    i_y = np.argmin(np.abs(yv[0, :, 0] - yp))
    i_z = np.argmin(np.abs(zv[0, :, 0] - zp))
    n_c = np.shape(C)[0]
    plt.figure(0)
    for i in range(n_c):
        ci = C[i]
        plt.plot(xv[:, 0, 0], ci[:, i_y, i_z])
        if not (xmax is None) and not (Cmax is None):
            print(xmax[i], Cmax[i])
            if not (xmax[i] is None) and not (Cmax[i] is None):
                plt.plot(xmax[i], Cmax[i], 'o')
    plt.show()
