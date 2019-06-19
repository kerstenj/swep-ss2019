import math
import logging as log

import numpy as np
import pandas as pd
from numba import njit

import csa


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
    else:
        return result / w


@njit
def get_distances(np_array, parameters, min_vec, max_vec):
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


@njit
def dist_to_cz(distances, cz):
    dist_cz = np.zeros(cz.shape[0])
    for i in range(cz.shape[0]):
        dist_cz[i] = distances[i, cz[i]]
    return dist_cz


def get_average_distance(distances, store):
    result=[]
    for i in store.cz:
        temp_cluster_array=store.df["cluster_center"][store.df["cluster_center"]==i]
        dist_cz = dist_to_cz(distances, store.df["cluster_center"].to_numpy())
        count_nodes=len(dist_Cz)
        sum = np.nansum(dist_Cz)/count_nodes
        # sum= statistics.median(dist_Cz)
        result.append(sum)

    dist_cz_all = dist_to_cz(distances, store.df["cluster_center"].to_numpy())
    # sum_all = np.nansum(dist_cz)


    return np.nansum(result)/len(store.cz)
    # return statistics.median(result)*statistics.median(dist_cz_all)




def get_best_dc(store, get_z, try_dc):
    # Calculate distances between all dates
    store.distances = get_distances(
        store.df.to_numpy(),
        store.meta.parameters,
        store.meta.min_vec.to_numpy(),
        store.meta.max_vec.to_numpy()
    )

    # Xalculate step different z
    if get_z:
        dc_low = 0.003
        dc_high = 0.2
        step = (dc_high - dc_low) / 100

    else:
        dc_low = dc_high = try_dc
        step = 1

    store.dc = dc_low

    z_list = list()
    dc_list = list()
    i = 0

    while store.dc <= dc_high:
        dc_list.append(store.dc)
        log.info(msg='-----------------')
        log.info(msg=f'{i}te Berechnung')
        i += 1

        cluster_center = csa.get_cluster_centers(store)
        store.cz = cluster_center

        z = get_average_distance(store.distances, store)
        log.info(msg=f'Z: {z}')
        z_list.append(z)
        store.dc += step

    test_series = pd.Series(z_list, index=dc_list)
    return test_series
