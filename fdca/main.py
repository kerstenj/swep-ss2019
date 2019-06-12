import numpy as np
import pandas as pd
import reader
import calcdc
import setting as s
import matplotlib.pyplot as plt
import openpyxl

#info Class for global information about the data
class infoC:
    def __init__(self,df):
        self.ZeilenAnz=len(df.index)
        self.SpaltenAnz=len(df.columns)
        self.MinVek=None
        self.MaxVek=None

s.init()

# turning all strings in categorical data to representative int:
def transformStringToInt():
    index=0
    for i in s.info.ParameterListe:
        if i == 1:
            s.df.iloc[:,index]=s.df.iloc[:,index].astype('category').cat.codes
        index+=1
    return

#diffrent test data input:

# s.df=reader.readTxtFileK('fdca/test2.txt')
s.df=reader.readTxtFileW('fdca/Aggregation.txt')
# s.df=reader.readTxtFileK('datasets/Iris/iris.data')
#only for this example:
# s.df = pd.DataFrame(data={'x':[0.8,0.81,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89,0.9,1.8,1.81,1.82,1.83,1.84,1.85,1.86,1.87,1.88,1.89,1.9], 'y': [0.8,0.81,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89,0.9,1.8,1.81,1.82,1.83,1.84,1.85,1.86,1.87,1.88,1.89,1.9]})
# hi=np.array([[0.8,0.81,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89,0.9,1.8,1.81,1.82,1.83,1.84,1.85,1.86,1.87,1.88,1.89,1.9], [0.8,0.81,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89,0.9,1.8,1.81,1.82,1.83,1.84,1.85,1.86,1.87,1.88,1.89,1.9]])
# print(hi)


s.info=infoC(s.df)


# deleting aditional information in the test data set

# del s.df["class"]
del s.df["CZ"]


# create a parameter list to map categorical and numerical data

#Parameter List: 0 - num   / 1- cat
# s.info.ParameterListe=np.array([0,0,0,0,1])
# s.info.ParameterListe=np.array([0,0,0,0])
s.info.ParameterListe=np.array([0,0])
#print(info.ZeilenAnz, info.SpaltenAnz, info.MinVek, info.MaxVek)

transformStringToInt()

# creating min and max vector to normalize numerical data
s.info.MaxVek=s.df.max()
s.info.MinVek=s.df.min()
# s.df.to_excel("hi.xlsx")

#choose to get a table with Z to dc or get a cluster for one dc

getZ=False
trydc=0.053
# trydc=0.053 1
# trydc=0.052 1
# trydc=0.048 1
# trydc=0.023
# trydc=0.07
# trydc=0.078
# trydc=0.093
# trydc=0.109
# trydc=0.046
# trydc=0.0392


#for testing returns a list of cluster centers
dc=calcdc.get_best_dc(getZ, trydc)

print(s.df.sort_values(by="maphd",axis=0,ascending=False))

# Z to dc table:
if getZ:
    plt.plot(dc)
    plt.show()

# cluster for trydc value:
else:

    fig, ax= plt.subplots()
    temp=s.df["ClusterCenter"]
    temp[s.df["ClusterCenter"]==s.df.index]=1

    # Aggregation:
    ax.scatter(s.df["x"],s.df["y"],c=temp)
    ax.set_xlabel('x')
    ax.set_ylabel('y')

    #Iris subtable:
    # ax.scatter(s.df["sepal length"],s.df["sepal width"],c=temp)
    # ax.set_xlabel('sepal length')
    # ax.set_ylabel('sepal width')

    ax.grid(True)
    fig.tight_layout()
    plt.show()
