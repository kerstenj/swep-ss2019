import pandas as pd
import distance
import setting as s

def density(): #aller Punkte

    s.df["Density"]=s.df.apply(getDensity, axis=1)


def getDensity(row):
    Dist=s.df.apply(distance.dist,node2=row, axis=1)
    return len(Dist[Dist < s.dc])

    #test=(Dist < s.dc).values.sum() - Laufzeitmäßig überprüfen

def maphd(): #Minimaler Abstand zu einem Punkt höherer Dichte /aller Punkte

    s.df["maphd"]=s.df.apply(getMaphd, axis=1)


def getMaphd(row):
    Dist=s.df.apply(distance.disthd,node2=row, axis=1) #ggf - bei Density speichern und hier wieder aufrufen
    print(Dist)
    return Dist.min()

#def calcCZ():


#     average=df["maphd"].mean()
#     CZ=list();
#     print(average)
#     for Node in df.itertuples(index=True, name='Pandas'):
#         print (getattr(Node, "maphd"), )
#         #if i["maphd"] > average:
#         #    print (i)
#

def getClusterZentren():


    density()
    maphd()
    # CZ=calcCZ()
    # #df=df.sort_values("maphd",0,False) #Sort by density
    print (s.df)
