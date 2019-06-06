import numpy as np
import pandas as pd
import CSA
import setting as s
from numba import njit

# import reader

# def dist(node1, node2, ParameterListe, MaxVek, MinVek): #Zwei expliziter Punkte
#     w = sum = j = 0
#
#     #print("Node1:", node1)
#     #print("Node2:", node2)
#
#
#     # Länge aufgrund von neuen Spalten variabel - andere Fehlerabfrage?!
#     # if not(len(node1)==len(node2) and len(node2)==len(max) and len(max)==len(min)):
#     #     return None
#
#     for i in ParameterListe:
#         if i == 0:
#             if not node1[j] and not node2[j]:
#                 w += 1
#                 sum += abs(node1[j] - node2[j]) / (MaxVek[j] - MinVek[j])
#         else:
#             if not node1[j] and not node2[j]:
#                 print("ups - kathegorische ditanz noch implementieren")
#         j+=1
#
#
#     if sum==0:
#         return None
#     return sum / w


# @njit
# def getDistances(df,ParameterListe, MaxVek, MinVek):
#     lenght=len(df)
#     res=np.empty(lenght, lenght)
#
#     for i in range(lenght):
#         temp=np.empty(lenght)
#         for j in range(lenght):
#             res[i,j]=dist(df[i], df[j],ParameterListe, MaxVek, MinVek)
#     #temp=np.vectorize(distance.dist)(s.df)
#     return res
#     #return pd.Series(temp)

def dist(node1, node2): #Zwei expliziter Punkte
    w = sum = j = 0

    for i in s.info.ParameterListe:

        if i == 0:
            if node1[j] != None and node2[j] != None:
                w += 1
                sum += abs(node1[j] - node2[j]) / (s.info.MaxVek[j] - s.info.MinVek[j])
        else:#i == 1:
            if node1[j] != None and node2[j] != None:
                w+=1
                if node1[j]==node2[j]:
                    sum+=0
                else:
                    sum+=1
        j+=1


    if sum==0:
        return None
    return sum / w

def getDistances(row):
    temp=s.df.apply(dist,node2=row, axis=1)
    #temp=np.vectorize(distance.dist)(s.df)
    return pd.DataFrame(temp)
    #return pd.Series(temp)

def distToCZ(df, CZ):
    return df.at[CZ, 0]

def getAverageDistance(CZ):

    distCz=np.vectorize(distToCZ)(CSA.df["Distances"], CSA.df["ClusterCenter"])
    print("Type")
    print(type(distCz))
    sum=np.nansum(distCz)
    print ()
    # for CZ in ClusterZent:
    #     temp=CSA.df[CSA.df["ClusterCenter"]==CZ]
    #     print("temp", CZ)
    #     print(temp[Distances].at[CZ, "Distances"])
    return sum/len(CZ)

def getbestdc():
    #Berechne Distanzen zwischen allen Datenpunkten
    s.df["Distances"]=s.df.apply(getDistances, axis=1)
    #s.df["Distances"]=getDistances(s.df.values,s.info.ParameterListe, s.info.MaxVek.values, s.info.MinVek.values)


    N=s.info.ZeilenAnz
    # pos other values
    # dclow=N*0.01
    # dchigh=N*0.2

    dclow=dchigh=0.25
    step=1
    #0.023   0.04   0.06

    # dclow=0.1
    # dchigh=1
    # step=(dchigh-dclow)/10


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

        ClusterZent=CSA.getClusterZentren(s.dc)
    #print(CSA.df.sort_values("ClusterCenter",axis=0,ascending=False))
        Z=getAverageDistance(ClusterZent)
        print("Z: ", Z)
        ListZ.append(Z)
        s.dc+=step

    TestDF=pd.Series(ListZ, index=Listdc)
    return TestDF
