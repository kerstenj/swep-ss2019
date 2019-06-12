import pandas as pd
import numpy as np
import setting
from numba import njit


dc = None
df = None
CZ = None


@njit
def get_density(dist, dc):
    dist_Cz = np.zeros(dist.shape[0])

    for i in range(dist.shape[0]):
        result = 0
        for j in range(i+1, dist.shape[0]):
            if dist[i, j] <= dc:
                dist_Cz[i] += 1
                dist_Cz[j] += 1
    return dist_Cz


@njit
def get_maphd_index(dist, dens):
    next_node = np.full(dist.shape[0], -1)

    for i in range(dist.shape[0]):
        for j in range(dist.shape[0]):
            # Distances where this density < other density or <= - without itself
            if dens[i] < dens[j]:
                if next_node[i] == -1:
                    next_node[i] = j
                elif dist[i, next_node[i]] > dist[i, j]:
                    next_node[i] = j

    return next_node


@njit
def get_maphd(dist, next_node):
    maphd = np.zeros(dist.shape[0])
    for i in range(dist.shape[0]):
        if next_node[i] == -1:
            maphd[i] = 1
        else:
            maphd[i] = dist[i, next_node[i]]

    return maphd


def calc_CZ(dist, df):
    CZ = []
    average_dens = df[0].mean()

    i = 0
    last_dens = []
    last_index = []
    while len(df[1]) > 0:

        if df[0, i] in last_dens:
            next_node_index = last_dens.index(df[0, i])
            setting.df.at[int(df[2, i]), "nextNode"] = last_index[next_node_index]
            df = np.delete(arr=df, obj=i, axis=1)
            continue
        if df[0, i] >= df[0].max():
            CZ.append(int(df[2, i]))
            last_dens.append(df[0, i])
            last_index.append(df[2, i])
            df = np.delete(arr=df, obj=i, axis=1)
        elif df[0, i] >= df[0].mean():
            CZ.append(int(df[2, i]))
            last_dens.append(df[0, i])
            last_index.append(df[2, i])
            df = np.delete(arr=df, obj=i, axis=1)
        else:
            break
    print("break")
    print(df)
    return CZ


@njit
def clustering(next_node, CZ):
    res = np.full(next_node.shape[0], -1)
    i = -1
    temp = []

    for cz in CZ:
        res[cz] = cz

    for todo in res:
        i += 1
        if todo == -1:
            k = i
            while res[k] == -1:
                temp.append(k)
                k = next_node[k]
            cz = res[k]
            while len(temp) != 0:
                res[temp.pop()] = cz

    return res


def get_cluster_centers(dc_p):
    global dc
    global df
    global CZ
    dc = dc_p
    df = setting.df

    print("Test dc: ", dc)
    print("...")

    # Berechne die Dichte der Datenpunkte abhängig von der Grenzdistanz dc
    df["Density"] = get_density(setting.Dist, dc)

    # maphd - Minimaler Abstand zu einem Punkt höherer Dichte (Delta im Paper)
    df["nextNode"] = get_maphd_index(setting.Dist, df["Density"].to_numpy())

    df["maphd"] = get_maphd(setting.Dist, df["nextNode"].to_numpy())

    temp_df = df.loc[:, ["Density", "maphd"]].sort_values(
        "maphd", axis=0, ascending=False
    )
    temp_df["Index"] = temp_df.index

    CZ = np.array(calc_CZ(setting.Dist, temp_df.to_numpy().T))
    print(CZ)

    df["ClusterCenter"] = clustering(df["nextNode"].to_numpy(), CZ)
    return CZ
