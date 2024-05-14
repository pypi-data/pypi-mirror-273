import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def plot_velocity_field(
    msh,
    vel,
    save_path=None,
    file_name=None,
    figsize=(20, 15),
    space_subsampling_rate=10,
    scale_arrow=1 / 1.025,
    width_arrow=0.2,
    vlim=None,
    title=None,
    format_out='pdf',
):
    """
    Plot the velocity field

    - input:
        * msh: object of the class MeshRect2D
        * vel: object of the class Velocity
        * save_path: string, None by default, contains the path to directory in which the figure is saved if not None
        * figsize: tuple, (20, 15) by default, contains the size of the figure
    - do:
        * plot on the whole domain the velocity field with an arrow representation of the velocity vector
        * save the figure in a pdf file if the save_path input is not None, show the figure otherwise
    """
    vel_field = vel.at_vertical_interface[::space_subsampling_rate, ::space_subsampling_rate, :]
    if vlim is None:
        vel_min = np.min(np.linalg.norm(vel_field, axis=2))
        vel_max = np.max(np.linalg.norm(vel_field, axis=2))
    else:
        vel_min = vlim[0]
        vel_max = vlim[1]
    # print(vel_min, vel_max)
    xm, ym = np.meshgrid(msh.x_vertical_interface[::space_subsampling_rate], msh.y[::space_subsampling_rate])
    fontsize = 25
    fig = plt.figure(0, figsize=figsize)
    plt.quiver(
        xm,
        ym,
        vel_field[:, :, 0],
        vel_field[:, :, 1],
        np.linalg.norm(vel_field, axis=2),
        cmap='jet',
        pivot='mid',
        units='x',
        width=width_arrow,
        scale=scale_arrow,
        clim=(vel_min, vel_max),
    )
    plt.xlabel('$x$ ($m$)', fontsize=fontsize)
    plt.ylabel('$y$ ($m$)', fontsize=fontsize)
    plt.tick_params(labelsize=fontsize - 5)
    if title is not None:
        plt.title(title, loc='center', fontsize=fontsize)
    cb_ax = fig.add_axes([0.92, 0.125, 0.02, 0.756])
    cbar = plt.colorbar(cax=cb_ax)
    cbar.ax.tick_params(direction='in', labelsize=fontsize - 5)
    cbar.set_label('$|U|$ ($m.s^{-1}$)', rotation=270, fontsize=fontsize, labelpad=40)
    if save_path is None:
        plt.show()
    else:
        # if the save directory does not exist, then it is created
        if not os.path.isdir(Path(save_path)):
            os.makedirs(Path(save_path))
        if file_name is None:
            file_name = 'velocity_field.' + format_out
        plt.savefig(Path(save_path) / file_name, format=format_out)
        plt.close('all')


def plot_diffusion_tensor(msh, diffu_coeff, save_path=None, figsize=(20, 15)):
    """
    Plot the diffusion tensor

    - input:
        * msh: object of the class MeshRect2D
        * diffu_coeff: object of the class DiffusionTensor
        * save_path: string, None by default, contains the path to directory in which the figure is saved if not None
        * figsize: tuple, (20, 15) by default, contains the size of the figure
    - do:
        * plot on the whole domain the four component of the diffusion tensor
        * save the figure in a pdf file if the save_path input is not None, show the figure otherwise
    """

    xm, ym = np.meshgrid(msh.x_vertical_interface, msh.y)

    cmax = np.max(diffu_coeff.at_vertical_interface[:, :, :, :])
    cmin = np.min(diffu_coeff.at_vertical_interface[:, :, :, :])

    fontsize = 25
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex=True, sharey=True, figsize=figsize)

    im = ax1.pcolormesh(xm, ym, diffu_coeff.at_vertical_interface[:, :, 0, 0], cmap="jet", vmin=cmin, vmax=cmax)
    ax1.set_ylabel("$y$ ($m$)", fontsize=fontsize)
    ax1.set_title("$K_{xx}$", fontsize=fontsize)
    ax1.tick_params(labelsize=fontsize - 5)

    ax4.pcolormesh(xm, ym, diffu_coeff.at_vertical_interface[:, :, 1, 1], cmap="jet", vmin=cmin, vmax=cmax)
    ax4.set_xlabel("$x$ ($m$)", fontsize=fontsize)
    ax4.set_title("$K_{yy}$", fontsize=fontsize)
    ax4.tick_params(labelsize=fontsize - 5)

    ax2.pcolormesh(xm, ym, diffu_coeff.at_vertical_interface[:, :, 0, 1], cmap="jet", vmin=cmin, vmax=cmax)
    ax2.set_title("$K_{xy}$", fontsize=fontsize)
    ax2.tick_params(labelsize=fontsize - 5)

    ax3.pcolormesh(xm, ym, diffu_coeff.at_vertical_interface[:, :, 1, 0], cmap="jet", vmin=cmin, vmax=cmax)
    ax3.set_xlabel("$x$ ($m$)", fontsize=fontsize)
    ax3.set_ylabel("$y$ ($m$)", fontsize=fontsize)
    ax3.set_title("$K_{yx}$", fontsize=fontsize)
    ax3.tick_params(labelsize=fontsize - 5)

    cb_ax = fig.add_axes([0.92, 0.125, 0.02, 0.756])
    cb = fig.colorbar(im, cax=cb_ax)
    cb.set_label(r"$K$ ($m^2.s^{-1}$)", rotation=270, fontsize=fontsize, labelpad=30)
    cb.ax.tick_params(labelsize=fontsize - 5)

    if save_path is None:
        plt.show()
    else:
        # if the save directory does not exist, then it is created
        if not os.path.isdir(Path(save_path)):
            os.makedirs(Path(save_path))
        plt.savefig(Path(save_path) / 'diffusion_tensor.pdf', format='pdf')
        plt.close('all')
