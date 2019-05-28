import numpy as np
import pandas as pd

def readTxtFileW(s):
    df=pd.read_csv(s, delim_whitespace=True)
    return df

def readTxtFileK(s):
    df=pd.read_csv(s)
    return df
