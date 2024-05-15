import numpy as np


def superlevel_set(threshold, s):
    return s > threshold


def intersection_superlevel_set(threshold, s_array):
    output = np.full(np.shape(s_array[0]), True)
    for s in s_array:
        output = output & superlevel_set(threshold, s)
    return output


def volume(domain, volume_cell):
    return np.sum(domain) * volume_cell


def volume_intersection_superlevel_set(threshold, s_array, volume_cell):
    domain = intersection_superlevel_set(threshold, s_array)
    return volume(domain, volume_cell)
