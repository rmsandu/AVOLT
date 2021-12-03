# -*- coding: utf-8 -*-
"""
@author: Raluca Sandu
"""

# -*- coding: utf-8 -*-
"""
@author: Raluca Sandu
"""

import os
import pandas as pd


input_folder_path = r"C:\develop\AVOLT\excel_data\ellipsoid"
files = os.listdir(input_folder_path)
data_frames = []

# %% aggregate and unpack distances
for input_file in files:
    print(input_file)
    input_filepath = os.path.join(input_folder_path, input_file)
    single_df = pd.read_excel(input_filepath, sheet_name='radiomics')
    data_frames.append(single_df)

data_aggregated = pd.concat(data_frames)
filepath_excel = "../plots/QAM_Inner_Outer_Ellipsoid.xlsx"
writer = pd.ExcelWriter(filepath_excel)
data_aggregated.to_excel(writer, sheet_name='radiomics', index=False, float_format='%.2f')
writer.save()


