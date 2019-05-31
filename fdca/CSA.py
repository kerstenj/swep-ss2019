import pandas as pd
import numpy as np
import setting as s

dc=None
df=None
CZ=None


def getDensity(row):
    global dc
    #Dist=s.df.apply(distance.dist,node2=row, axis=1)
    Dist=row["Distances"]
    #print("Dichte: ", Dist[Dist < s.dc].count() )
    return Dist[Dist < dc].count()

    #(Dist < s.dc).values.sum() - Laufzeitmäßig überprüfen

def getMaphdIndex(row):
    global df

    # Distances where this Density < other Density
    temp=row[s.info.SpaltenAnz+1][row[s.info.SpaltenAnz+2] < df["Density"] ]

    if (temp.empty):
        return None

    return temp.idxmin()[0]

def getMaphd(row):
    # maphd Index
    index=row[s.info.SpaltenAnz+3]
    if pd.isna(index):
       return None

    # Distances
    temp=row[s.info.SpaltenAnz+1][0]

    return temp[index]



def calcCZ():
    global df
    CZ=list()
    average=df["maphd"].mean()

    Dens=df["Density"].sort_values(axis=0,ascending=False)
    maphd=df["maphd"].sort_values(axis=0,ascending=False)

    maphdIndex=0
    #prob. faster iteration possible - needed?
    for row_index, row in Dens.items():

        if row_index==maphd.index[maphdIndex]:
            CZ.append(row_index)
            maphdIndex+=1
            continue
        if pd.isna(maphd[row_index]):
            CZ.append(row_index)
            continue
        if maphd[row_index]>average:
            CZ.append(row_index)

        break

        #print("index: ", row_index,"item: ", row)


    return CZ

def Clustering(row):
    # print("Start Rows:")
    # print(row, row.name)
    global CZ
    global df


    if row.name in CZ:
        return row.name
    else:
        return Clustering(df.loc[row["nextNode"],:])


def ClusteringforIndex(index):
    global CZ
    if index in CZ:
        return index
    else:
        return ClusteringforIndex()

def getAverageDistance():


    return


def getClusterZentren(dcP):
    global dc
    global df
    global CZ
    dc=dcP
    df=s.df

    print("Test dc: ", dc)
    print("...")

    #Berechne die Dichte der Datenpunkte abhängig von der Grenzdistanz dc
    df["Density"]=df.apply(getDensity, axis=1)


     # maphd - Minimaler Abstand zu einem Punkt höherer Dichte
    df["nextNode"]=df.apply(getMaphdIndex, axis=1)
    df["maphd"]=df.apply(getMaphd, axis=1)


    #delete Distances-Column
    df.drop("Distances", axis=1, inplace=True)


    CZ=calcCZ()

    df["ClusterCenter"]=df.apply(Clustering, axis=1)

    print(df.sort_values("ClusterCenter",axis=0,ascending=False))
    print(CZ)
    return CZ
    # #df=df.sort_values("maphd",0,False) #Sort by density
    #print (s.df)



#Wichtige Funktionen:
#
#   itterieren über df in anderen df
#   s.df["Distances"].apply(printitnow)
#
#
#Ausgabe eines df in einem anderen df:
#print (s.df["Distances"][0])
