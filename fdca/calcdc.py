import numpy as np
import pandas as pd
import CSA
import setting as s

def getbestdc():

    N=s.info.ZeilenAnz
    dclow=N*0.01
    dchigh=N*0.2
    ClusterZent=CSA.getClusterZentren()
