import pandas as pd

def read_txt_whitespace(path):
    df = pd.read_csv(path, delim_whitespace=True)
    return df

def read_txt_comma(path):
    df = pd.read_csv(path)
    return df