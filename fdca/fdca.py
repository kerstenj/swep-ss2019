import logging as log
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import fdca.calcdc as calcdc
import fdca.visualisation_new as vi
from fdca.storage import Storage


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


def execute(df, parameters, try_dc):
    """
    Executes the FDCA algorithm of the given dataframe using the parameters.
    Returns a series containing the associated cluster of each date.
    """
    # Initialisation
    transform_str_to_int(df, parameters)
    store = Storage(df, parameters)

    # Calculate clusters
    calcdc.calculate_cluster(store, try_dc)

    # Logs a list of cluster centers
    log.info(msg=store.df.sort_values(by="maphd", axis=0, ascending=False).to_string())

    # Plots the data
    vi.plot_3d_test(store, "sepal length", "sepal width", "petal length", "petal width")

    # z to dc plot:
    return (store.df["cluster_center"], store.cz)


def calculate_z(df, parameters, dc_low=0, dc_high=0.2, step_count=200):
    """

    """
    # Initialisation
    transform_str_to_int(df, parameters)
    store = Storage(df, parameters)

    #
    temp = calcdc.get_best_dc(store, dc_low, dc_high, step_count)

    # Plots a graph of the calculated z values
    # vi.plot_line(temp)

    # Calculate dc to z mapping
    return temp
