import numpy as np
import pandas as pd
import CSA
import setting as s
import distance


def getDistances(row):
    temp=s.df.apply(distance.dist,node2=row, axis=1)
    return pd.DataFrame(temp)
    #return pd.Series(temp)

def getbestdc():
    #Berechne Distanzen zwischen allen Datenpunkten
    s.df["Distances"]=s.df.apply(getDistances, axis=1)

    N=s.info.ZeilenAnz
    dclow=N*0.01
    dchigh=N*0.2
    ClusterZent=CSA.getClusterZentren(s.dc)
