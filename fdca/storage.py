import numpy as np

class Storage:
    """
    Stores the dataframe and computed values of the algorithm.
    """
    def __init__(self, df, parameters):
        self.df = df                                # Dataframe
        self.dc = None                              # Used dc value
        self.distances = None                       # Distances between all points
        self.cz = None                              # 
        self.row_count = len(df.index)              # Row count of the dataframe e.g. number of dates
        self.column_count = len(df.columns)         # Column count of the dataframe e.g. number of parameters per date
        self.min_vec = df.min()                     # Minimum date vector of the dataframe
        self.max_vec = df.max()                     # Maximum date vector of the dataframe
        self.parameters = np.array(parameters)      # List that describes the type (0 = continuos, 1 = categorical) of each parameter
