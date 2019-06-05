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
        self.MinVek=df.min()
        self.MaxVek=df.max()
        self.ParameterListe=df.columns

s.init()


s.df=reader.readTxtFileK('fdca/test.txt')
#s.df=reader.readTxtFileW('fdca/Aggregation.txt')
#s.df=reader.readTxtFileK('datasets/Iris/iris.data')
#only for this example:



s.info=infoC(s.df)

#Parameter List: 0 - num   / 1- cat
#s.info.ParameterListe=[1,1,1,1]
s.info.ParameterListe=[1,1]
#print(info.ZeilenAnz, info.SpaltenAnz, info.MinVek, info.MaxVek)

dc=calcdc.getbestdc()

print(s.df["x"],s.df["y"],s.df["Distances"][0],s.df["Density"],s.df["nextNode"])
# plt.plot(dc)
# plt.show()



fig, ax= plt.subplots()
scatter = ax.scatter(s.df["x"],s.df["y"],c=s.df["ClusterCenter"])

ax.set_xlabel('x')
ax.set_ylabel('y')

ax.grid(True)
fig.tight_layout()
plt.show()
