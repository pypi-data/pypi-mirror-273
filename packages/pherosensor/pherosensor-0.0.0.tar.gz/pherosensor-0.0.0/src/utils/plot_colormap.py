import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import ticker


def plot_colormap(
    msh, xy_map, label, unit, cmap="jet", title=None, map_bound=None, save_path=None, file_name=None, file_format='pdf', figsize=(20, 15)
):
    """
    Plot a given physical quantity

    - input:
        * msh: object of the class MeshRect2D
        * xy_map: numpy array of shape (mesh.y.size, mesh.x.size), contains the mean value of the physical quantity in the cells
        * label: string, contains the label of the physical quantity, can be in LaTeX format
        * unit: string, contains the unit of the physical quantity, can be in LaTeX format
        * cmap: string, "jet" by default, contains the name of the colormap to use
        * title: string, None by default, contains the title of the figure, can be in LaTeX format
        * map_bound: tuple, contains the lower and upper boundary we want to impose to the colormap
        * save_path: string, None by default, contains the path to directory in which the figure is saved if not None
        * file_name: string, None by default, contains the name of the filein which the figure is saved if save_path is not None
        * file_format: string, 'pdf' by default, contains the format of the file in which the figure is saved if save_path is not None
        * figsize: tuple, (20, 15) by default, contains the size of the figure
    - do:
        * plot on the whole domain the given physical quantity
        * save the figure in a file if the save_path input is not None, show the figure otherwise
    """
    if map_bound is None:
        vmin = np.min(xy_map)
        vmax = np.max(xy_map)
    else:
        vmin = map_bound[0]
        vmax = map_bound[1]
    fontsize = 25
    fig = plt.figure(0, figsize=figsize)
    plt.pcolormesh(msh.x, msh.y, xy_map, cmap=cmap, vmin=vmin, vmax=vmax)
    plt.xlabel("$x$ ($m$)", fontsize=fontsize)
    plt.ylabel("$y$ ($m$)", fontsize=fontsize)
    plt.xlim(np.min(msh.x), np.max(msh.x))
    plt.ylim(np.min(msh.y), np.max(msh.y))
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    plt.tick_params(labelsize=fontsize - 5)
    if title is not None:
        plt.title(title, loc='center', fontsize=fontsize)
    cb_ax = fig.add_axes([0.92, 0.15, 0.02, 0.69])
    cbar = plt.colorbar(cax=cb_ax)
    cbar.set_label(rf"${label}$ (${unit}$)", rotation=270, fontsize=fontsize, labelpad=30)
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
        if file_name is None:
            file_name = label
        plt.savefig(Path(save_path) / f"{file_name}.{file_format}", format=file_format)
        plt.close('all')


def plot_colormap_all_timestep(
    msh, t, txy_map, label, unit, cmap="jet", save_path='./plot/plot_all_timestep/', figsize=(20, 15), restart_ite=0
):
    """
    Plot and save a given physical quantity at every time step

    - input:
        * msh: object of the class MeshRect2D
        * t: numpy array, contains all the time at which the physical quantity is plotted
        * txy_map:
            numpy array of shape (t.size, mesh.y.size, mesh.x.size),
            contains the mean value of the physical quantity in the cells at every time step
        * label: string, contains the label of the physical quantity, can be in LaTeX format
        * unit: string, contains the unit of the physical quantity, can be in LaTeX format
        * cmap: string, "jet" by default, contains the name of the colormap to use
        * save_path: string, './plot/plot_all_timestep/' by default, contains the path to directory in which all the figures are saved
    - do:
        * plot on the whole domain and at every time step the given physical quantity
        * save the figures in png files
    """

    # if the save directory does not exist, then it is created
    if not os.path.isdir(save_path):
        os.makedirs(save_path)

    # all the figures have the same colormap boundary
    cmin = np.min(txy_map)
    cmax = np.max(txy_map)
    mb = [cmin, cmax]

    t = t[restart_ite:]
    txy_map = txy_map[restart_ite:, :, :]
    for i in range(t.size):
        sys.stdout.write(f'\r ite = {np.str(i+1+restart_ite)} / {np.str(t.size)}')
        sys.stdout.flush()
        xy_map = txy_map[i, :, :]
        # the time is printed in the figure as title
        title = f't = {"{:.2f}".format(t[i])} s'
        # the name of the files contains the index of the time step, so that the alphabetic order is also the time order
        fname = f'{label}_ite{"{0:04d}".format(i+restart_ite)}'
        plot_colormap(
            msh,
            xy_map,
            label,
            unit,
            cmap=cmap,
            title=title,
            map_bound=mb,
            save_path=save_path,
            file_name=fname,
            file_format='png',
            figsize=figsize,
        )
