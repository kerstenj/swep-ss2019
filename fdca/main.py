import numpy as np
import pandas as pd
import reader
import calcdc
import setting as s
import matplotlib.pyplot as plt

class infoC:
    def __init__(self,df):
        self.ZeilenAnz=len(df.index)
        self.SpaltenAnz=len(df.columns)
        self.MinVek=None
        self.MaxVek=None

s.init()

# turning all Strings in categorical data to representative int:
def transformStringToInt():
    index=0
    for i in s.info.ParameterListe:
        if i == 1:
            s.df.iloc[:,index]=s.df.iloc[:,index].astype('category').cat.codes
        index+=1
    return

#s.df=reader.readTxtFileK('fdca/test.txt')
# s.df=reader.readTxtFileW('fdca/Aggregation.txt')
s.df=reader.readTxtFileK('datasets/Iris/iris.data')
#only for this example:



s.info=infoC(s.df)

#Parameter List: 0 - num   / 1- cat
s.info.ParameterListe=np.array([0,0,0,0,1])


# del s.df["class"]
# del s.df["CZ"]


# s.info.ParameterListe=np.array([0,0,0,0])
# s.info.ParameterListe=np.array([0,0])
#print(info.ZeilenAnz, info.SpaltenAnz, info.MinVek, info.MaxVek)

transformStringToInt()


s.info.MaxVek=s.df.max()
s.info.MinVek=s.df.min()

getZ=False
trydc=0.25
# 0.0108
# 0.0088
# trydc=0.00497
# trydc=0.059
# trydc=0.319
# trydc=0.309
# trydc=0.015

dc=calcdc.getbestdc(getZ, trydc)

#print(s.df["x"],s.df["y"],s.df["Distances"][0],s.df["Density"],s.df["nextNode"])
# print(s.df["Distances"][0],s.df["Density"],s.df["maphd"],s.df["nextNode"])
# print("means: ", s.df["Density"].mean(),s.df["maphd"].mean())

if getZ:
    plt.plot(dc)
    plt.show()
else:
    fig, ax= plt.subplots()
    temp=s.df["ClusterCenter"]
    temp[s.df["ClusterCenter"]==s.df.index]=1
    ax.scatter(s.df["x"],s.df["y"],c=temp)
    ax.set_xlabel('x')
    ax.set_ylabel('y')

    ax.grid(True)
    fig.tight_layout()
    plt.show()
