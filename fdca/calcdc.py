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
<<<<<<< HEAD
                # euclid norm:
                # sum += (abs(node1[j] - node2[j]) / (MaxVek[j] - MinVek[j]))**2
                sum += abs(node1[j] - node2[j]) / (MaxVek[j] - MinVek[j])
=======
                result += (abs(node1[j] - node2[j]) / (max_vec[j] - min_vec[j]))**2
>>>>>>> 07230df4f6a555310a08ab6fecd3886151ebe748

        else:
            if not (np.isnan(node1[j]) or np.isnan(node2[j])):
                w += 1
                if node1[j] == node2[j]:
                    result += 1
        j += 1

    if result == 0:
        return 0
<<<<<<< HEAD
    # euclid norm:
    # return math.sqrt(sum) / w
    return sum / w

=======

    return math.sqrt(result) / w
>>>>>>> 07230df4f6a555310a08ab6fecd3886151ebe748


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
<<<<<<< HEAD
def distToCZ(Dist, ClusterMappingVec):
    #ClusterMappingVec - vector with the mapping of all datapoints to their cluster centers
    distCz=np.zeros(ClusterMappingVec.shape[0])
    for i in range(ClusterMappingVec.shape[0]):
        distCz[i]=Dist[i,ClusterMappingVec[i]]
    return distCz
=======
def dist_to_CZ(dist, CZ):
    dist_Cz = np.zeros(CZ.shape[0])
    for i in range(CZ.shape[0]):
        dist_Cz[i] = dist[i, CZ[i]]
    return dist_Cz
>>>>>>> 07230df4f6a555310a08ab6fecd3886151ebe748


def get_average_distance(CZ):

<<<<<<< HEAD
    sum=np.nansum(distCz)

    # maybe without /len(CZ)
    return sum/len(CZ)

def getbestdc(getZ, trydc):
    #calculate distances between all datapoints
    s.Dist=getDistances(s.df.to_numpy(), s.info.ParameterListe, s.info.MinVek.to_numpy(), s.info.MaxVek.to_numpy())

    #berechnete "Dreiecksmatrix" zu "quadratischer Matrix" für bessere Adressierung:
    s.Dist+=s.Dist.T
=======
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
>>>>>>> 07230df4f6a555310a08ab6fecd3886151ebe748

    # "Dreiecksmatrix" zu "quadratischer Matrix":
    setting.Dist += setting.Dist.T

<<<<<<< HEAD
    #calculate step diffrent Z
    if getZ:
        dclow=0
        dchigh=0.2
        step=(dchigh-dclow)/100
=======
    N = setting.info.ZeilenAnz
>>>>>>> 07230df4f6a555310a08ab6fecd3886151ebe748

    if get_z:
        dc_low = 0.003
        dc_high = 0.2
        step = (dc_high - dc_low) / 100

<<<<<<< HEAD
    
    s.dc=dclow
=======
    else:
        dc_low = dc_high = try_dc
        step = 1

    setting.dc = dc_low
>>>>>>> 07230df4f6a555310a08ab6fecd3886151ebe748

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

<<<<<<< HEAD
        ClusterZent=CSA.getClusterCenters(s.dc)
        s.CZ=ClusterZent

        Z=getAverageDistance(ClusterZent)
        print("Z: ", Z)
        # ListZ.append(Z)
        ListZ.append(len(ClusterZent))
        s.dc+=step
=======
        Z = get_average_distance(cluster_center)
        print("Z: ", Z)
        z_list.append(Z)
        setting.dc += step
>>>>>>> 07230df4f6a555310a08ab6fecd3886151ebe748

    TestDF = pd.Series(z_list, index=dc_list)
    return TestDF
