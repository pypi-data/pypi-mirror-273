import os
import sys
from pathlib import Path

import imageio


def generate_gif(images_path='./plot/plot_all_timestep/', save_path='./plot/', file_name='output'):
    """
    generate a gif file from png files contained in a given directory
    * images_path: string, './plot/plot_all_timestep/' by default, contains the path of the directory in which the figures are
    * save_path: string, './plot/' by default, contains the path of the directory in which the gif file will be saved
    * file_name string, 'output' by default, name of the file in which the gif will be saved

    - do:
        * open and concatenate in the alphabetic order the files contained in the given images' directory
        * save the array of images as a gif in the given save directory
    """

    images = []
    nfile = len([f for f in os.listdir(Path(images_path)) if os.path.isfile(Path(images_path) / f)])
    ifile = 0
    for filename in sorted(os.listdir(Path(images_path))):
        if os.path.isfile(Path(images_path) / filename):
            sys.stdout.write(f'\r {"{:.2f}".format(100*ifile/nfile)}% : {filename}')
            sys.stdout.flush()
            images.append(imageio.imread(Path(images_path) / filename))
            ifile += 1
    sys.stdout.write('\r 100% : saving the gif')
    sys.stdout.flush()
    imageio.mimsave(Path(save_path) / f'{file_name}.gif', images)
