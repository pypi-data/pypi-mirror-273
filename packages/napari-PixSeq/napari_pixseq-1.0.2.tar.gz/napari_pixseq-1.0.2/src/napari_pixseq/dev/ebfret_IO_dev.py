


import pandas as pd
import numpy as np


path = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\Code\MatLab\ebfret-gui-master-Sep2023\datasets\simulated-K04-N350-traces-K04.dat"


df = pd.read_csv(path, sep = "  ", header=None)


def infer_efficiency(data, assumed_IA=100):

    E = np.array(data)
    IA = np.full_like(E, assumed_IA)
    ID = IA * (1 - E) / E
    
    return ID, IA


data = df.iloc[:,0]