import numpy as np
import pandas as pd
import CSA
import setting as s
from numba import njit
import math

@njit
def dist(node1, node2, ParameterListe, MaxVek, MinVek): #Zwei expliziter Punkte
    w = sum = j = 0

    #print("Node1:", node1)
    #print("Node2:", node2)


    # Länge aufgrund von neuen Spalten variabel - andere Fehlerabfrage?!
    # if not(len(node1)==len(node2) and len(node2)==len(max) and len(max)==len(min)):
    #     return None
    for i in ParameterListe:
        if i == 0:
            if not (np.isnan(node1[j]) or np.isnan(node2[j])):
                w += 1
                # euclid norm:
                # sum += (abs(node1[j] - node2[j]) / (MaxVek[j] - MinVek[j]))**2
                sum += abs(node1[j] - node2[j]) / (MaxVek[j] - MinVek[j])

        else:
            if not (np.isnan(node1[j]) or np.isnan(node2[j])):
                w+=1
                if node1[j] == node2[j]:
                    sum += 1
        j+=1


    if sum==0:
        return 0
    # euclid norm:
    # return math.sqrt(sum) / w
    return sum / w



@njit
def getDistances(npArray,ParameterListe, MinVek, MaxVek):

    res=np.zeros((npArray.shape[0],npArray.shape[0]))

    for i in range(npArray.shape[0]):
        for j in range(i+1, npArray.shape[0]):
            res[i,j]=dist(npArray[i], npArray[j], ParameterListe, MaxVek, MinVek)
    #temp=np.vectorize(distance.dist)(s.df)
    return res
    #return pd.Series(temp)

@njit
def distToCZ(Dist, ClusterMappingVec):
    #ClusterMappingVec - vector with the mapping of all datapoints to their cluster centers
    distCz=np.zeros(ClusterMappingVec.shape[0])
    for i in range(ClusterMappingVec.shape[0]):
        distCz[i]=Dist[i,ClusterMappingVec[i]]
    return distCz

def getAverageDistance(CZ):

    distCz=distToCZ(s.Dist, CSA.df["ClusterCenter"].to_numpy())

    sum=np.nansum(distCz)

    # maybe without /len(CZ)
    return sum/len(CZ)

def getbestdc(getZ, trydc):
    #calculate distances between all datapoints
    s.Dist=getDistances(s.df.to_numpy(), s.info.ParameterListe, s.info.MinVek.to_numpy(), s.info.MaxVek.to_numpy())

    #berechnete "Dreiecksmatrix" zu "quadratischer Matrix" für bessere Adressierung:
    s.Dist+=s.Dist.T

    N=s.info.ZeilenAnz
    # pos other values
    # dclow=N*0.01
    # dchigh=N*0.2

    #calculate step diffrent Z
    if getZ:
        dclow=0
        dchigh=0.2
        step=(dchigh-dclow)/100

    else:
        dclow=dchigh=trydc
        step=1

    
    s.dc=dclow

    ListZ=list();
    Listdc=list();
    i=0

    while s.dc<=dchigh:
        Listdc.append(s.dc)
        print()
        print("-----------------")
        print()
        print(i,". te Berechnung")
        i+=1

        ClusterZent=CSA.getClusterCenters(s.dc)
        s.CZ=ClusterZent

        Z=getAverageDistance(ClusterZent)
        print("Z: ", Z)
        # ListZ.append(Z)
        ListZ.append(len(ClusterZent))
        s.dc+=step

    TestDF=pd.Series(ListZ, index=Listdc)
    return TestDF
