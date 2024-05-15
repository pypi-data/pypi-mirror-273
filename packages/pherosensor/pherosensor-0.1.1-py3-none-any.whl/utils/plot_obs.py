import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import ticker


def plot_obs(msh, t, obs, figsize=(20, 15), cmap="jet", save_path=None, file_format='pdf', cbar_dim=[0.92, 0.15, 0.02, 0.69]):
    """
    Plot and save the observations at a given time step

    - input:
        * msh: object of the class MeshRect2D
        * t: float, contains the time at which the observations plotted
        * obs: object of the class Obs, contains the observations we want to plot
        * cmap: string, "jet" by default, contains the name of the colormap to use
        * save_path: string, './plot/plot_all_timestep/' by default, contains the path to directory in which all the figures are saved
        * file_format: string, 'pdf' by default, contains the format of the file in which the figure is saved if save_path is not None
        * figsize: tuple, (20, 15) by default, contains the size of the figure
    - do:
        * plot on the observations at a given time step, the points not observed are left white
        * save the figures in a file
    """

    index_t = np.argmin(np.abs(t - msh.t_array))
    if index_t in obs.index_obs_to_index_time_est:
        index_x_est = []
        index_y_est = []
        index_obs = obs.index_time_est_to_index_obs[index_t]
        for i in index_obs:
            index_x_est.append(np.argmin(np.abs(msh.x - obs.X_obs[i, 0])))
            index_y_est.append(np.argmin(np.abs(msh.y - obs.X_obs[i, 1])))
        out = np.empty((msh.y.size, msh.x.size))
        out.fill(np.nan)
        for i_x, i_y, i_obs in zip(index_x_est, index_y_est, index_obs):
            out[i_y, i_x] = obs.d_obs[i_obs]
        fontsize = 25
        fig = plt.figure(0, figsize=figsize)
        plt.pcolormesh(msh.x, msh.y, out, cmap=cmap)
        plt.xlabel("$x$ ($m$)", fontsize=fontsize)
        plt.ylabel("$y$ ($m$)", fontsize=fontsize)
        plt.xlim(np.min(msh.x), np.max(msh.x))
        plt.ylim(np.min(msh.y), np.max(msh.y))
        ax = plt.gca()
        ax.set_aspect('equal', adjustable='box')
        plt.tick_params(labelsize=fontsize - 5)
        plt.title(f'at t = {"{:.2f}".format(t)} s', loc='center', fontsize=fontsize)
        cb_ax = fig.add_axes(cbar_dim)
        cbar = plt.colorbar(cax=cb_ax)
        cbar.set_label(r"$m^{obs}$", rotation=270, fontsize=fontsize, labelpad=30)
        cbar.ax.tick_params(labelsize=fontsize - 5)
        cbar.ax.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True, useOffset=True))
        cbar.ax.ticklabel_format(style='sci', scilimits=(0, 0))
        cbar.ax.yaxis.offsetText.set_fontsize(fontsize - 5)
        if save_path is None:
            plt.show()
        else:
            # if the save directory does not exist, then it is created
            if not os.path.isdir(Path(save_path)):
                os.makedirs(Path(save_path))
            plt.savefig(Path(save_path) / f"obs.{file_format}", format=file_format)
            plt.close('all')

    else:
        print("No observation was made at the given time")
