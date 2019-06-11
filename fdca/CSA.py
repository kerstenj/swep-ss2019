import pandas as pd
import numpy as np
import setting as s
from numba import njit

dc=None
df=None
CZ=None

@njit
def getDensity(Dist ,dc):
    distCz=np.zeros(Dist.shape[0])

    for i in range(Dist.shape[0]):
        sum=0
        for j in range(i+1, Dist.shape[0]):
            if Dist[i,j] <= dc:
                distCz[i]+=1
                distCz[j]+=1
    return distCz

@njit
def getMaphdIndex(Dist, Dens):
    nextNode=np.full(Dist.shape[0],-1)


    for i in range(Dist.shape[0]):
        for j in range(Dist.shape[0]):
            # Distances where this density < other density or <= - without itself
            #if Dens[i]<=Dens[j] and i!=j:
            if Dens[i]<Dens[j]:
                if nextNode[i]==-1:
                    nextNode[i]=j
                elif Dist[i,nextNode[i]] > Dist[i,j]:
                    nextNode[i]=j

    return nextNode

@njit
def getMaphd(Dist,nextNode):
    maphd=np.zeros(Dist.shape[0])
    for i in range (Dist.shape[0]):
        if nextNode[i]==-1:
            maphd[i]=1
        else:
            maphd[i]=Dist[i,nextNode[i]]

    return maphd

# def calcCZ(Dist, df):
#     CZ=[]
#     #size=Dist.shape[0]
#     averageDens=df[0].mean()
#
#     print()
#     print()
#     i=0
#     Test=0
#     while len(df[1])>0 :
#         #if maphd = max(maphd) (paper - delta)
#         print()
#         print()
#         print("DP: ", Test)
#         Test+=1
#         print(df[0,i],df[1,i],df[2,i])
#         print("max",df[1].max())
#         print("average",df[1].mean())
#         if df[1,i]>=df[1].max():
#             print("greater max")
#             CZ.append(int(df[2,i]))
#             df=np.delete(arr=df,obj=i,axis=1)
#             #Laufzeitüerprüfung bei größeren Itterationen mit numba:
#             # df=deleteDP(df,i,size)
#             # size-=1
#         # if maphd >= average maphd
#         elif df[1,i]>=df[1].mean():
#             print("greater average")
#             CZ.append(int(df[2,i]))
#             df=np.delete(arr=df,obj=i,axis=1)
#             # df=deleteDP(df,i,size)
#             # size-=1
#         else:
#             break
#     print("break")
#     print(df)
#     return CZ

def calcCZ(Dist, df):
    CZ=[]
    # size=Dist.shape[0]
    averageDens=df[0].mean()

    # print()
    # print()
    i=0
    # Test=0
    lastDens=[]
    lastIndex=[]
    while len(df[1])>0 :
        #if maphd = max(maphd) (paper - delta)
        # print()
        # print()
        # print("DP: ", Test)
        # Test+=1
        # print(df[0,i],df[1,i],df[2,i])
        # print("max",df[0].max())
        # print("average",df[0].mean())


        if df[0,i] in lastDens:
            # print()
            # print("Übersprungen: ", df[2,i])
            nextNodeIndex=lastDens.index(df[0,i])
            # print(s.df.at[int(df[2,i]),"nextNode"])
            s.df.at[int(df[2,i]),"nextNode"]=lastIndex[nextNodeIndex]
            # print(s.df.at[int(df[2,i]),"nextNode"])
            df=np.delete(arr=df,obj=i,axis=1)

            continue
        if df[0,i]>=df[0].max():
            # print("greater max")
            CZ.append(int(df[2,i]))
            lastDens.append(df[0,i])
            lastIndex.append(df[2,i])
            df=np.delete(arr=df,obj=i,axis=1)
            #Laufzeitüerprüfung bei größeren Itterationen mit numba:
            # df=deleteDP(df,i,size)
            # size-=1
        # if maphd >= average maphd
        elif df[0,i]>=df[0].mean():
            # print("greater average")
            CZ.append(int(df[2,i]))
            lastDens.append(df[0,i])
            lastIndex.append(df[2,i])
            df=np.delete(arr=df,obj=i,axis=1)
            # df=deleteDP(df,i,size)
            # size-=1
        else:
            break
    print("break")
    print(df)
    return CZ

# def calcCZ(Dist, df):
#     CZ=[]
#     #size=Dist.shape[0]
#     averageDist=df[1].mean()
#     maxDist=df[1].max()
#
#     i=0
#     Test=0
#     while len(df[1])>0 :
#         if df[1,i]>=df[1].max():
#             CZ.append(int(df[2,i]))
#             df=np.delete(arr=df,obj=i,axis=1)
#
#         elif df[1,i]>=averageDist:
#
#             CZ.append(int(df[2,i]))
#             df=np.delete(arr=df,obj=i,axis=1)
#
#         else:
#             break
#
#     return CZ


@njit
def Clustering(nextNode, CZ):
    res=np.full(nextNode.shape[0],-1)
    i=-1
    temp=[]

    for cz in CZ:
        res[cz]=cz

    for todo in res:
        i+=1
        if todo == -1:
            k=i
            while res[k]==-1:
                temp.append(k)
                k=nextNode[k]
            cz=res[k]
            while (len(temp)!=0):
                res[temp.pop()]=cz

    return res

def getClusterZentren(dcP):
    global dc
    global df
    global CZ
    dc=dcP
    df=s.df

    print("Test dc: ", dc)
    print("...")

    #Berechne die Dichte der Datenpunkte abhängig von der Grenzdistanz dc
    df["Density"]=getDensity(s.Dist, dc)


    # maphd - Minimaler Abstand zu einem Punkt höherer Dichte (Delta im Paper)
    # nextNode = index of maphd
    df["nextNode"]=getMaphdIndex(s.Dist, df["Density"].to_numpy())

    # print(df.nextNode)
    # print(df[df["nextNode"]==-1])
    # print(df["Density"].sort_values(axis=0,ascending=False))

    df["maphd"]=getMaphd(s.Dist,df["nextNode"].to_numpy())

    TempDf=df.loc[:, ["Density", "maphd"]].sort_values("maphd", axis=0, ascending=False)
    TempDf["Index"]=TempDf.index

    CZ=np.array(calcCZ(s.Dist, TempDf.to_numpy().T))
    print(CZ)
    #CZ=calcCZ(s.Dist, TempDf["Density"].to_numpy(), TempDf["maphd"].to_numpy(), TempDf["Index"].to_numpy())


    df["ClusterCenter"]=Clustering(df["nextNode"].to_numpy(),CZ)

    # print(df.sort_values("ClusterCenter",axis=0,ascending=False))
    # print("CZ: ", str(CZ))

    return CZ
