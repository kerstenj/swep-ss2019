class Storage:
    """
    Stores the dataframe and computed values of the algorithm.
    """
    def __init__(self, df):
        self.df = df
        self.meta = Meta(df)
        self.dc = None
        self.distances = None
        self.cz = None




class Meta:
    """
    Contains metadata about the used dataframe.
    """

    def __init__(self, df):
        self.row_count = len(df.index)
        self.column_count = len(df.columns)
        self.min_vec = df.min()
        self.max_vec = df.max()
        self.parameters = None
