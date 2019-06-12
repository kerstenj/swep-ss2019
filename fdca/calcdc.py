import math

import numpy as np
import pandas as pd
from numba import njit

import CSA
import setting


@njit
def dist(node1, node2, parameters, max_vec, min_vec):  # Zwei expliziter Punkte
    w = result = j = 0

    for i in parameters:
        if i == 0:
            if not (np.isnan(node1[j]) or np.isnan(node2[j])):
                w += 1
                result += (abs(node1[j] - node2[j]) / (max_vec[j] - min_vec[j]))**2

        else:
            if not (np.isnan(node1[j]) or np.isnan(node2[j])):
                w += 1
                if node1[j] == node2[j]:
                    result += 1
        j += 1

    if result == 0:
        return 0

    return math.sqrt(result) / w


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

    return res


@njit
def dist_to_CZ(dist, CZ):
    dist_Cz = np.zeros(CZ.shape[0])
    for i in range(CZ.shape[0]):
        dist_Cz[i] = dist[i, CZ[i]]
    return dist_Cz


def get_average_distance(CZ):

    dist_Cz = dist_to_CZ(setting.Dist, CSA.df["ClusterCenter"].to_numpy())

    sum = np.nansum(dist_Cz)
    print()
    return sum / len(CZ)


def get_best_dc(get_z, try_dc):
    # Berechne Distanzen zwischen allen Datenpunkten
    setting.Dist = get_distances(
        setting.df.to_numpy(),
        setting.info.ParameterListe,
        setting.info.MinVek.to_numpy(),
        setting.info.MaxVek.to_numpy()
    )

    # "Dreiecksmatrix" zu "quadratischer Matrix":
    setting.Dist += setting.Dist.T

    N = setting.info.ZeilenAnz

    if get_z:
        dc_low = 0.003
        dc_high = 0.2
        step = (dc_high - dc_low) / 100

    else:
        dc_low = dc_high = try_dc
        step = 1

    setting.dc = dc_low

    z_list = list()
    dc_list = list()
    i = 0

    while setting.dc <= dc_high:
        dc_list.append(setting.dc)
        print()
        print("-----------------")
        print()
        print(i, ". te Berechnung")
        i += 1

        cluster_center = CSA.get_cluster_centers(setting.dc)
        setting.CZ = cluster_center

        Z = get_average_distance(cluster_center)
        print("Z: ", Z)
        z_list.append(Z)
        setting.dc += step

    TestDF = pd.Series(z_list, index=dc_list)
    return TestDF
