import pandas as pd
import setting as s
from numba import njit
# import reader


@njit
def dist(node1, node2): #Zwei expliziter Punkte
    w = sum = j = 0

    #print("Node1:", node1)
    #print("Node2:", node2)


    # Länge aufgrund von neuen Spalten variabel - andere Fehlerabfrage?!
    # if not(len(node1)==len(node2) and len(node2)==len(max) and len(max)==len(min)):
    #     return None

    for i in s.info.ParameterListe:

        if i == 1:
            if node1[j] != None and node2[j] != None:
                w += 1
                sum += abs(node1[j] - node2[j]) / (s.info.MaxVek[j] - s.info.MinVek[j])
        else:
            if node1[j] != None and node2[j] != None:
                print("Fehler - kathegorische ditanz noch implementieren")
        j+=1


    if sum==0:
        return None
    return sum / w
