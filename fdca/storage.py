import numpy as np


class Storage:
    """
    Stores the dataframe and computed values of the algorithm.
    """
    def __init__(self, df, parameters):
        # Dataframe
        self.df = df
        # Used dc value
        self.dc = None
        # Distances between all points
        self.distances = None
        # 
        self.cz = None
        # Row count of the dataframe e.g. number of dates
        self.row_count = len(df.index)
        # Column count of the dataframe e.g. number of parameters per date
        self.column_count = len(df.columns)
        # Minimum date vector of the dataframe
        self.min_vec = df.min()
        # Maximum date vector of the dataframe
        self.max_vec = df.max()
        # List that describes the type (0 = continuos, 1 = categorical) of each parameter
        self.parameters = np.array(parameters)
