import pandas as pd
import distance
import setting as s


def getDensity(row):
    #Dist=s.df.apply(distance.dist,node2=row, axis=1)
    Dist=row["Distances"]
    #print("Dichte: ", Dist[Dist < s.dc].count() )
    return Dist[Dist < s.dc].count()

    #(Dist < s.dc).values.sum() - Laufzeitmäßig überprüfen

def getMaphd(row):
    maphdVek=list();

    #maphd=s.df.apply(helpMaphd, node2=row, axis=1)
    temp=row[s.info.SpaltenAnz+1][row[s.info.SpaltenAnz+2] < s.df["Density"] ]

    if (temp.empty):
        maphdVek.append(1)
        maphdVek.append(None)
    else:
        maphdVek.append(temp.min()[0])
        maphdVek.append(temp.idxmin()[0])

    print (maphdVek)
    #maphd=row["Distances"][row["Density"]<].idxmin() #ggf - bei Density speichern und hier wieder aufrufen

    #maphd.append(row["Distances"][maphd[0]])
    #print (maphdVek)
    #print(Dist)
    return maphdVek


def getDistances(row):
    temp=s.df.apply(distance.dist,node2=row, axis=1)

    return pd.DataFrame(temp)

#def calcCZ():


#     average=df["maphd"].mean()

def getClusterZentren():
    #Berechne Distanzen zwischen allen Datenpunkten
    s.df["Distances"]=s.df.apply(getDistances, axis=1)
    #print(s.df["Distances"])

    #Berechne die Dichte der Datenpunkte abhängig von der Grenzdistanz dc
    s.df["Density"]=s.df.apply(getDensity, axis=1)

    #print(s.df["Density"])
     # maphd - Minimaler Abstand zu einem Punkt höherer Dichte
    maphdVek=s.df.apply(getMaphd, axis=1)
    print(maphdVek)
    #s.df["maphd"]
    # CZ=calcCZ()
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
