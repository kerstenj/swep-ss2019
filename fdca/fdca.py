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

    # z to dc plot:
    return (store.df["cluster_center"], store.cz)

def calculate_z(df, parameters, dc_low=0, dc_high=0.2, step_count=200):
    """

    """
    # Initialisation
    transform_str_to_int(df, parameters)
    store = Storage(df, parameters)

    # Calculate dc to z mapping
    return calcdc.get_best_dc(store, dc_low, dc_high)


execute(reader.read_txt_whitespace('fdca\Aggregation.txt'), [0, 0],  0.0471)
calculate_z(reader.read_txt_whitespace('fdca\Aggregation.txt'), [0, 0])