"""
This module contains functions for calculating the dc value.
"""

import math
import logging as log
import numpy as np
import pandas as pd
from numba import njit

import fdca.csa as csa


@njit
def dist(vec_a, vec_b, parameters, max_vec, min_vec, euclid_norm=True):
    """
    Calculates the distance between two data vectors a and b.
    """
    w = result = j = 0

    for i in parameters:
        if i == 0:
            if not (np.isnan(vec_a[j]) or np.isnan(vec_b[j])):
                w += 1

                if euclid_norm:
                    result += (abs(vec_a[j] - vec_b[j]) / (max_vec[j] - min_vec[j]))**2
                else:
                    result += abs(vec_a[j] - vec_b[j]) / (max_vec[j] - min_vec[j])

        else:
            if not (np.isnan(vec_a[j]) or np.isnan(vec_b[j])):
                w += 1
                if vec_a[j] == vec_b[j]:
                    result += 1
        j += 1

    if result == 0:
        return 0

    if euclid_norm:
        return math.sqrt(result) / w

    return result / w


@njit
def get_distances(np_array, parameters, min_vec, max_vec):
    """
    Returns an array for every distance between two data points.
    """
    res = np.zeros((np_array.shape[0], np_array.shape[0]))
    for i in range(np_array.shape[0]):
        for j in range(i+1, np_array.shape[0]):
            res[i, j] = dist(
                np_array[i], np_array[j],
                parameters,
                max_vec, min_vec
            )

    # "Dreiecksmatrix" zu "quadratischer Matrix":
    return res + res.transpose()


def get_z(store):
    """
    Returns a Z value for a given dc and dataframe.
    """
    result = []

    for i in store.centers:
        temp_df = store.df["density"][store.df["cluster_center"] == i]
        sum = np.sum(temp_df) / len(temp_df)
        result.append(sum)

    return np.nansum(result) / len(store.centers)


def get_dc_z_map(store, dc_low, dc_high, step_count):
    """
    Returns the List of Z values for a dataframe.
    """
    # Calculate distances between all dates
    store.distances = get_distances(
        store.df.to_numpy(),
        store.parameters,
        store.min_vec.to_numpy(),
        store.max_vec.to_numpy()
    )
    # Calculate step different z
    step = (dc_high - dc_low) / step_count

    store.dc = dc_low

    z_list = list()
    dc_list = list()
    i = 0

    while store.dc <= dc_high:
        dc_list.append(store.dc)
        log.info(msg='-----------------')
        log.info(msg='{i}te Berechnung')
        i += 1

        cluster_center = csa.get_centers(store)
        store.centers = cluster_center

        z = get_z(store)
        log.info(msg=f'Z: {z}')

        z_list.append(z)
        store.dc += step

    test_series = pd.Series(z_list, index=dc_list)
    return test_series


def calculate_cluster(store, try_dc):
    """
    Calculate cluster centers for a given dc.
    """
    # Calculate distances between all dates
    store.distances = get_distances(
        store.df.to_numpy(),
        store.parameters,
        store.min_vec.to_numpy(),
        store.max_vec.to_numpy()
    )
    store.dc = try_dc

    cluster_center = csa.get_centers(store)
    store.centers = cluster_center
