import numpy as np
import logging as log
import pandas as pd
import reader
import calcdc
import visualisation
from storage import Storage
import matplotlib.pyplot as plt
# import openpyxl


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

def execute(df, parameter_list, try_dc):
    transform_str_to_int(df, parameter_list)
    store = Storage(df, parameter_list)

    calcdc.calculate_cluster(store, try_dc)

    # for testing returns a list of cluster centers
    log.info(msg=store.df.sort_values(by="maphd", axis=0, ascending=False).to_string())

    # visualisation.plot_2D(store)
    visualisation.plot_2D(store)

    #print(store.df.sort_values(by="density", axis=0, ascending=False)[store.df["cluster_center"]==store.df.index]["density"])

    # z to dc plot:
    return (store.df,store.cz)

def calculate_z(df, parameter_list, dc_low=0, dc_high=0.2):
    transform_str_to_int(df, parameter_list)
    store = Storage(df, parameter_list)

    return calcdc.get_best_dc(store, dc_low, dc_high)

# hi=False
# hi=True
#
# if hi:
#
#     plt.plot(calculate_z(reader.read_txt_whitespace('flame.txt'), [0, 0]))
#     # plt.plot(calculate_z(reader.read_txt_whitespace('fdca/flame.txt'), [0, 0]))
#     # plt.plot(calculate_z(reader.read_txt_whitespace('fdca/Aggregation.txt'), [0, 0]))
#     # plt.plot(calculate_z(reader.read_txt_comma('datasets/Iris/iris.data'), [0, 0, 0, 0 ,1]))
#     plt.show()
#
# else:
#
#     # df,cz=execute(reader.read_txt_whitespace('fdca/Aggregation.txt'), [0, 0],  0.0471)
#     # df,cz=execute(reader.read_txt_whitespace('fdca/flame.txt'), [0, 0],  0.06758)
#     df,cz=execute(reader.read_txt_whitespace('fdca/jain.txt'), [0, 0],  0.02835)
#     #0.021
#     #
#     # cluster for try_dc value:
#     fig, ax = plt.subplots()
#     temp = df["cluster_center"].copy()
#     temp[df["cluster_center"] == df.index] = 1
#     #
#     # # Aggregation:
#     ax.scatter(df["x"], df["y"], c=temp)
#     ax.set_xlabel('x')
#     ax.set_ylabel('y')
#     #
#     # # Iris subtable:
#     # ax.scatter(s.df["sepal length"],s.df["sepal width"],c=temp)
#     # ax.set_xlabel('sepal length')
#     # ax.set_ylabel('sepal width')
#     #
#     #
#     ax.grid(True)
#     fig.tight_layout()
#     plt.show()


execute(reader.read_txt_whitespace('flame.txt'), [0, 0, 0],  0.05)
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
