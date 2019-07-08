import numpy as np
import logging as log
import pandas as pd

import fdca.calcdc as calcdc
import fdca.visualisation as vi
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

    # z to dc plot:
    return (store.df, store.centers)


def calculate_z(df, parameters, dc_low=0, dc_high=0.2, step_count=200):
    """
    Calculate a measure value Z for every dc between dc_low and dc_high
    with step_count steps between them.
    """
    # Initialisation
    transform_str_to_int(df, parameters)
    store = Storage(df, parameters)

    # Calculate dc to z mapping
    return calcdc.get_dc_z_map(store, dc_low, dc_high, step_count)
