"""
This module contains the functions for clustering.
"""

import logging as log

import numpy as np
from numba import njit


@njit
def get_density(distances, dc):
    """
    Returns the density of each date calculated by the distances and the dc value.
    """
    dist_cz = np.zeros(distances.shape[0])

    for i in range(distances.shape[0]):
        for j in range(i+1, distances.shape[0]):
            if distances[i, j] <= dc:
                dist_cz[i] += 1
                dist_cz[j] += 1
    return dist_cz


@njit
def get_maphd_index(distances, density, dc):
    """
    Returns for every datapoint the nearest data point with a higher density.
    """
    next_node = np.full(distances.shape[0], -1)

    for i in range(distances.shape[0]):
        for j in range(distances.shape[0]):
            if density[i] < density[j]:
                if next_node[i] == -1:
                    next_node[i] = j
                else:
                    if distances[i, next_node[i]] > distances[i, j]:
                        next_node[i] = j
            elif density[i] == density[j] and i < j:
                if next_node[i] == -1:
                    next_node[i] = j
                elif distances[i, next_node[i]] > distances[i, j] and distances[i, j] <= dc:
                    next_node[i] = j
    return next_node


@njit
def get_maphd(distances, next_nodes):
    """
    Returns the distance to the nearest data point with a higher density.
    """
    maphd = np.zeros(distances.shape[0])
    for i in range(distances.shape[0]):
        if next_nodes[i] == -1:
            maphd[i] = 1
        else:
            maphd[i] = distances[i, next_nodes[i]]

    return maphd


@njit
def clustering(next_nodes, cz):
    """
    Returns a list of the cluster center indices for every data point.
    """
    result = np.full(next_nodes.shape[0], -1)
    i = -1
    temp = []

    for cz_element in cz:
        result[cz_element] = cz_element

    for todo in result:
        i += 1
        if todo == -1:
            k = i
            while result[k] == -1:
                temp.append(k)
                k = next_nodes[k]
            cz_element = result[k]
            while len(temp) != 0:
                result[temp.pop()] = cz_element

    return result


def calculate_centers(df):
    """
    Returns the cluster centers.
    """
    cz = []
    while len(df[1]) != 0:
        if df[0, 0] >= df[0].max():
            cz.append(int(df[2, 0]))
            df = np.delete(arr=df, obj=0, axis=1)
        elif df[0, 0] >= df[0].mean():
            cz.append(int(df[2, 0]))
            df = np.delete(arr=df, obj=0, axis=1)
        else:
            break
    return cz


def get_centers(store):
    """
    Returns the cluster centers as a list.
    """
    log.info('Test dc: {store.dc}')
    log.info('...')

    # Calculate the density of the dates dependant on dc
    store.df['density'] = get_density(store.distances, store.dc)

    # maphd - Minimaler Abstand zu einem Punkt höherer Dichte (Delta im Paper)
    store.df['next_node'] = get_maphd_index(
        store.distances,
        store.df['density'].to_numpy(),
        store.dc
    )

    store.df['maphd'] = get_maphd(
        store.distances,
        store.df['next_node'].to_numpy()
    )

    temp_df = store.df.loc[:, ['density', 'maphd']].sort_values(
        'maphd', axis=0, ascending=False
    )
    temp_df['index'] = temp_df.index

    store.centers = np.array(calculate_centers(
        temp_df.to_numpy().T
    ))

    store.df['cluster_center'] = clustering(
        store.df['next_node'].to_numpy(),
        store.centers
    )

    return store.centers
