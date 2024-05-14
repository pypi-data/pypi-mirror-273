import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as npl


def plot_mean_error_ctrl_comparison_vs_ite(
    case_dict,
    ctrl_target,
    optim_iter_start=0,
    optim_iter_end=-1,
    flag_domain=None,
    ordre_norm=2,
    ylabel=None,
    save_path=None,
    file_name=None,
    file_format='pdf',
    figsize=(20, 15),
):
    if flag_domain is None:
        flag_domain = np.full(ctrl_target.value.shape, True, dtype=bool)
    if ylabel is None:
        ylabel = r'$RMSE(s)=\sqrt{\frac{1}{|\Omega|T}\int_\Omega\int_0^T(s-s_t)^2dtdxdy}~~(m^2.s^{-1})$'

    fontsize = 25

    plt.figure(figsize=figsize)

    for key in case_dict.keys():
        case = case_dict[key]
        mean_error = [
            npl.norm(s[flag_domain] - ctrl_target.value[flag_domain], ord=ordre_norm) / (len(s[flag_domain]) ** (1 / ordre_norm))
            for s in case['S vs ite']
        ]
        plt.plot(mean_error[optim_iter_start:optim_iter_end], case['ls'], label=case['label'])

    plt.xlabel(r'iteration', fontsize=fontsize)
    plt.ylabel(ylabel, fontsize=fontsize)
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
            file_name = f'mean_error_ordre_{ordre_norm}_comparison'
        plt.savefig(Path(save_path) / f"{file_name}.{file_format}", format=file_format)
        plt.close('all')
