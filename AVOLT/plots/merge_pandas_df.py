# -*- coding: utf-8 -*-
"""
@author: Raluca Sandu
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import ylabel, xticks, subplots, setp, title
import numpy as np


def fix_my_data(x):
    idx = x.find('L')
    return x[idx+1:]


filepath_distances = "QAM_Distances_Radiomics.xlsx"
filepath_radiomics = "Radiomics_MAVERRIC_RedCap_May2020.xlsx"
df_radiomics = pd.read_excel(filepath_radiomics)
df_distances = pd.read_excel(filepath_distances)
df_radiomics.Lesion = df_radiomics["Lesion"].apply(lambda x: x[x.find('L')+1:])
df_radiomics.Lesion = df_radiomics["Lesion"].apply(lambda x: str(x))
df_distances.Lesion = df_distances["Lesion"].apply(lambda x: str(x))
# df_radiomics.Patient = df_radiomics["Patient"].apply(lambda x: str(x))
# df_distances.Patient = df_distances["Patient"].apply(lambda x: str(x))

df_full = df_distances.merge(df_radiomics, how='left', left_on=['Patient', 'Lesion'],  right_on=['Patient', 'Lesion'])

filepath_excel = "QAM_Distances_Radiomics_Chemo.xlsx"
writer = pd.ExcelWriter(filepath_excel)
df_full.to_excel(writer, sheet_name='all', index=False, float_format='%.2f')
writer.save()



