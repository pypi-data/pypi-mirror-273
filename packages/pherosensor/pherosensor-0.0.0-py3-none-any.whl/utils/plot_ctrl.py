import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import ticker


def trajectory(x, y, msh, U):
    x_out = [x]
    y_out = [y]
    x_p = x
    y_p = y
    i_x = 1
    i_y = 1
    u = (U.at_vertical_interface[:, 1:, 0] + U.at_vertical_interface[:, :-1, 0]) * 0.5
    v = (U.at_horizontal_interface[1:, :, 1] + U.at_horizontal_interface[:-1, :, 1]) * 0.5
    while i_x > 0 and i_y > 0:
        i_x = np.argmin(np.abs(msh.x - x_p))
        i_y = np.argmin(np.abs(msh.y - y_p))
        x_p -= msh.dt * u[i_y, i_x]
        y_p -= msh.dt * v[i_y, i_x]
        x_out.append(x_p)
        y_out.append(y_p)
    return x_out, y_out


def plot_ctrl_map(
    msh,
    t,
    ctrl_map,
    ctrl_target_map=None,
    obs=None,
    trajectory_U=None,
    cmap="jet",
    title=None,
    map_bound=None,
    label='s',
    save_path=None,
    file_name=None,
    file_format='pdf',
    figsize=(20, 15),
):
    index_t = np.argmin(np.abs(t - msh.t_array))
    ctrl_current_t = np.copy(ctrl_map[index_t, :, :])

    if title is None:
        title = f'at t = {"{:.2f}".format(msh.t_array[index_t])} s'
    unit = "g.m^{-2}.s^{-1}"
    fontsize = 25
    if map_bound is None:
        vmin = np.min(ctrl_current_t)
        vmax = np.max(ctrl_current_t)
    else:
        vmin = map_bound[0]
        vmax = map_bound[1]

    fig, ax = plt.subplots(figsize=figsize)

    if obs is not None:
        if index_t in obs.index_obs_to_index_time_est:
            index_obs_x = []
            index_obs_y = []
            index_obs = obs.index_time_est_to_index_obs[index_t]
            for i in index_obs:
                index_obs_x.append(np.argmin(np.abs(msh.x - obs.X_obs[i, 0])))
                index_obs_y.append(np.argmin(np.abs(msh.y - obs.X_obs[i, 1])))
                ctrl_current_t[index_obs_y, index_obs_x] = np.nan
        else:
            print("No observation was made at the given time")

    plt.pcolormesh(msh.x, msh.y, ctrl_current_t, cmap=cmap, vmin=vmin, vmax=vmax)

    if ctrl_target_map is not None:
        ctrl_target_current_t = np.copy(ctrl_target_map[index_t, :, :])
        contour = ax.contour(msh.x, msh.y, ctrl_target_current_t, colors='k', linestyles='dashed', levels=0, linewidths=4)
        fmt = {}
        strs = [rf'$s_t={str(np.max(ctrl_target_current_t))}$']
        for lev, s in zip(contour.levels, strs):
            fmt[lev] = s
        ax.clabel(contour, contour.levels, inline=True, fontsize=fontsize, fmt=fmt)

    if trajectory_U is not None:
        if index_t in obs.index_obs_to_index_time_est:
            xy_traj = {}
            index_obs = obs.index_time_est_to_index_obs[index_t]
            for i in index_obs:
                xc, yc = trajectory(obs.X_obs[i, 0], obs.X_obs[i, 1], msh, trajectory_U)
                xy_traj[str(i)] = [xc, yc]
        for key in xy_traj.keys():
            Xc = xy_traj[key]
            plt.plot(Xc[0], Xc[1], 'w')

    plt.xlabel("$x$ ($m$)", fontsize=fontsize)
    plt.ylabel("$y$ ($m$)", fontsize=fontsize)
    plt.title(title, loc='center', fontsize=fontsize)
    plt.xlim(np.min(msh.x), np.max(msh.x))
    plt.ylim(np.min(msh.y), np.max(msh.y))
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    plt.tick_params(labelsize=fontsize - 5)
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


def plot_ctrl(
    msh,
    t,
    ctrl,
    ctrl_target=None,
    obs=None,
    trajectory_U=None,
    cmap="jet",
    title=None,
    map_bound=None,
    label='s',
    save_path=None,
    file_name=None,
    file_format='pdf',
    figsize=(20, 15),
):
    ctrl_map = ctrl.value.reshape((msh.t_array.size, msh.y.size, msh.x.size))
    if ctrl_target is not None:
        ctrl_target_map = ctrl_target.reshape((msh.t_array.size, msh.y.size, msh.x.size))
    else:
        ctrl_target_map = None
    plot_ctrl_map(
        msh,
        t,
        ctrl_map,
        ctrl_target_map=ctrl_target_map,
        obs=obs,
        trajectory_U=trajectory_U,
        cmap="jet",
        title=title,
        map_bound=map_bound,
        label=label,
        save_path=save_path,
        file_name=file_name,
        file_format='pdf',
        figsize=(20, 15),
    )


def plot_ctrl_all_timestep(msh, ctrl, ctrl_target=None, obs=None, label='s', cmap="jet", save_path='./plot/plot_all_timestep/'):
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
    cmin = np.min(ctrl.value)
    cmax = np.max(ctrl.value)
    mb = [cmin, cmax]

    ctrl_map = ctrl.value.reshape((msh.t_array.size, msh.y.size, msh.x.size))
    if ctrl_target is not None:
        ctrl_target_map = ctrl_target.reshape((msh.t_array.size, msh.y.size, msh.x.size))
    else:
        ctrl_target_map = None

    for i in range(msh.t_array.size):
        sys.stdout.write(f'\r ite = {np.str(i+1)} / {np.str(msh.t_array.size)}')
        sys.stdout.flush()
        # the time is printed in the figure as title
        title = f't = {"{:.2f}".format(msh.t_array[i])} s'
        # the name of the files contains the index of the time step, so that the alphabetic order is also the time order
        fname = f'{label}_ite{"{0:04d}".format(i)}'
        plot_ctrl_map(
            msh,
            msh.t_array.size[i],
            ctrl_map,
            ctrl_target=ctrl_target_map,
            obs=obs,
            cmap=cmap,
            title=title,
            map_bound=mb,
            label=label,
            save_path=save_path,
            file_name=fname,
            file_format='png',
            figsize=(20, 15),
        )
