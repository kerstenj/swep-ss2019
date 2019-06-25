import numpy as np
import logging as log
import pandas as pd
import reader
import calcdc
from storage import Storage
import matplotlib.pyplot as plt
import openpyxl


def transform_str_to_int(df, parameters):
    """
    Transforms all categorical dates in the given dataframe
    to representative integers.
    """
    index = 0
    for i in parameters:
        if i == 1:
            df.iloc[:, index] = df.iloc[:, index].astype('category').cat.codes
        index += 1
    return


def execute(df, parameter_list, try_dc):
    store = Storage(df, parameter_list)

    transform_str_to_int(store.df, store.parameters)

    calcdc.calculate_cluster(store, try_dc)

    # for testing returns a list of cluster centers
    log.info(msg=store.df.sort_values(by="maphd", axis=0, ascending=False).to_string())

    #print(store.df.sort_values(by="density", axis=0, ascending=False)[store.df["cluster_center"]==store.df.index]["density"])
    # z to dc plot:
    return (store.df["cluster_center"],store.cz)

def calculate_z(df, parameter_list, dc_low=0, dc_high=0.2):
    store = Storage(df, parameter_list)

    transform_str_to_int(store.df, store.parameters)
    return calcdc.get_best_dc(store, dc_low, dc_high)



execute(reader.read_txt_whitespace('fdca/Aggregation.txt'), [0, 0],  0.0471)
calculate_z(reader.read_txt_whitespace('fdca/Aggregation.txt'), [0, 0])

"""
df, cz = call()
store = Storage(reader.read_txt_whitespace('Aggregation.txt'))

diffrent test data input:

s.df=reader.readTxtFileK('fdca/test2.txt')
s.df=reader.readTxtFileK('datasets/Iris/iris.data')
only for this example:
s.df = pd.DataFrame(data={'x':[0.8,0.81,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89,0.9,1.8,1.81,1.82,1.83,1.84,1.85,1.86,1.87,1.88,1.89,1.9], 'y': [0.8,0.81,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89,0.9,1.8,1.81,1.82,1.83,1.84,1.85,1.86,1.87,1.88,1.89,1.9]})
hi=np.array([[0.8,0.81,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89,0.9,1.8,1.81,1.82,1.83,1.84,1.85,1.86,1.87,1.88,1.89,1.9], [0.8,0.81,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89,0.9,1.8,1.81,1.82,1.83,1.84,1.85,1.86,1.87,1.88,1.89,1.9]])
print(hi)


deleting aditional information in the test data set

del s.df["class"]
del store.df["CZ"]


create a parameter list to map categorical and numerical data

Parameter List: 0 - num   / 1- cat
s.info.ParameterListe=np.array([0,0,0,0,1])
s.info.ParameterListe=np.array([0,0,0,0])
store.parameters = np.array([0, 0])
print(info.ZeilenAnz, info.SpaltenAnz, info.MinVek, info.MaxVek)

creating min and max vector to normalize numerical data
s.df.to_excel("hi.xlsx")

choose to get a table with Z to dc or get a cluster for one dc

get_z = False
try_dc = 0.053
trydc=0.053 1
trydc=0.052 1
trydc=0.048 1
trydc=0.023
trydc=0.07
trydc=0.078
trydc=0.093
trydc=0.109
trydc=0.046
trydc=0.0392
"""
