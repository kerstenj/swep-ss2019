import numpy as np

class Storage:
    """
    Stores the dataframe and computed values of the algorithm.
    """
    def __init__(self, df, parameters):
        self.df = df
        self.dc = None
        self.distances = None
        self.cz = None
        self.row_count = len(df.index)
        self.column_count = len(df.columns)
        self.min_vec = df.min()
        self.max_vec = df.max()
        self.parameters = np.array(parameters)
