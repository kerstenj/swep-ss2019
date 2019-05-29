import pandas as pd
import numpy as np
import distance
import setting as s


def getDensity(row):
    #Dist=s.df.apply(distance.dist,node2=row, axis=1)
    Dist=row["Distances"]
    #print("Dichte: ", Dist[Dist < s.dc].count() )
    return Dist[Dist < s.dc].count()

    #(Dist < s.dc).values.sum() - Laufzeitmäßig überprüfen

def getMaphdIndex(row):

    temp=row[s.info.SpaltenAnz+1][row[s.info.SpaltenAnz+2] < s.df["Density"] ]

    if (temp.empty):
        return None

    return temp.idxmin()[0]

def getMaphd(row):
    index=row[s.info.SpaltenAnz+3]
    if pd.isna(index):
       return None

    temp=row[s.info.SpaltenAnz+1][0]

    return temp[index]


def getDistances(row):
    temp=s.df.apply(distance.dist,node2=row, axis=1)

    return pd.DataFrame(temp)
    #return pd.Series(temp)

def calcCZ():
    CZ=list()
    average=s.df["maphd"].mean()

    Dens=s.df["Density"].sort_values(axis=0,ascending=False)
    maphd=s.df["maphd"].sort_values(axis=0,ascending=False)
    # performance option:
    # Dens.to_numpy()
    #
    # #Dens=s.df["Density"].sort_values("Density",0,False)
    #print(Dens)
    # # print(Dens[0])
    # print(Dens.iat[0])
    # print(Dens.iat[1])
    # print(Dens.iat[2])
    # print()
    # print(list(Dens.index.values))
    # print(maphd)
    # print(maphd.keys())
    # print(maphd.index[0])
    i=0

    for row_index, row in Dens.items():

        if row_index==maphd.index[i]:
            CZ.append(row_index)
            i+=1
            continue
        if pd.isna(maphd[row_index]):
            CZ.append(row_index)
            continue
        if maphd[row_index]>average:
            CZ.append(row_index)

        break

        #print("index: ", row_index,"item: ", row)


    return CZ

def getClusterZentren():
    #Berechne Distanzen zwischen allen Datenpunkten
    s.df["Distances"]=s.df.apply(getDistances, axis=1)


    #Berechne die Dichte der Datenpunkte abhängig von der Grenzdistanz dc
    s.df["Density"]=s.df.apply(getDensity, axis=1)


     # maphd - Minimaler Abstand zu einem Punkt höherer Dichte
    s.df["nextNode"]=s.df.apply(getMaphdIndex, axis=1)

    s.df["maphd"]=s.df.apply(getMaphd, axis=1)
    # print(s.df["nextNode"])
    # print(s.df["maphd"])
    # print(s.df["Distances"])

    #delete Distances-Column
    s.df.drop("Distances", axis=1, inplace=True)
    print(s.df)

    CZ=calcCZ()
    print(CZ)
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
