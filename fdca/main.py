import numpy as np
import pandas as pd
import reader
import calcdc
import setting as s

class infoC:
    def __init__(self,df):
        self.ZeilenAnz=len(df.index)
        self.SpaltenAnz=len(df.columns)
        self.MinVek=df.min()
        self.MaxVek=df.max()
        self.ParameterListe=df.columns

s.init()

s.dc=0.5
s.df=reader.readTxtFileW('fdca/AggregationTest2.txt')
s.info=infoC(s.df)
s.info.SpaltenAnz=2 #Nur für Test !! # TODO: delete
s.info.ParameterListe=["num","num"]
#print(info.ZeilenAnz, info.SpaltenAnz, info.MinVek, info.MaxVek)
dc=calcdc.getbestdc()
