"""
This module contains the functions for executing the FDCA.
"""

import fdca.calcdc as calcdc
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
    # Save categorical data before int transform
    categorical_data = {}
    for idx, parameter in enumerate(parameters):
        if parameter == 0: continue
        column_name = df.columns[idx]
        categorical_data[column_name] = df[column_name]

    transform_str_to_int(df, parameters)
    store = Storage(df, parameters)

    # Calculate clusters
    calcdc.calculate_cluster(store, try_dc)

    # Restore categorical data
    for column_name, data in categorical_data.items():
        store.df[column_name] = data
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
