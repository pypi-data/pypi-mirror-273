import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def plot_cost(j_obs, j_reg, norm_noise, label_reg, ls_reg, save_path=None, file_name=None, file_format='pdf', figsize=(20, 15)):
    j = np.array(j_obs)
    for key in j_reg.keys():
        j += np.array(j_reg[key])

    fontsize = 25

    plt.figure(figsize=figsize)

    plt.plot(j, 'c', label='$j$')
    plt.plot(j_obs, 'b', label='$j_{obs}$')
    for key in j_reg.keys():
        plt.plot(j_reg[key], ls_reg[key], label=rf'$\alpha_{{{label_reg[key]}}}j_{{{label_reg[key]}}}$')
    plt.plot(norm_noise * np.ones((len(j_obs))), 'k--', label=r'$||\epsilon||_{L^2}^2$')
    plt.xlabel(r'iteration', fontsize=fontsize)
    plt.ylabel(r'$j$', fontsize=fontsize)
    plt.tick_params(labelsize=fontsize - 5)
    plt.yscale('log')
    plt.legend(fontsize=fontsize)

    if save_path is None:
        plt.show()
    else:
        # if the save directory does not exist, then it is created
        if not os.path.isdir(Path(save_path)):
            os.makedirs(Path(save_path))
        if file_name is None:
            file_name = 'cost'
        plt.savefig(Path(save_path) / f"{file_name}.{file_format}", format=file_format)
        plt.close('all')


def plot_cost_obs_comparison(case_dict, save_path=None, file_name=None, file_format='pdf', figsize=(20, 15)):
    fontsize = 25

    plt.figure(figsize=figsize)

    for key in case_dict.keys():
        case = case_dict[key]
        plt.plot(case['j_obs'], case['ls'], label=case['label'])

    plt.xlabel(r'iteration', fontsize=fontsize)
    plt.ylabel(r'$j_{obs}$', fontsize=fontsize)
    plt.tick_params(labelsize=fontsize - 5)
    plt.yscale('log')
    plt.legend(fontsize=fontsize)

    if save_path is None:
        plt.show()
    else:
        # if the save directory does not exist, then it is created
        if not os.path.isdir(Path(save_path)):
            os.makedirs(Path(save_path))
        if file_name is None:
            file_name = 'cost_obs_comparison'
        plt.savefig(Path(save_path) / f"{file_name}.{file_format}", format=file_format)
        plt.close('all')
