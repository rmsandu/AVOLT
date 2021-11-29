# -*- coding: utf-8 -*-
"""
@author: Raluca Sandu
"""

import os
import pandas as pd


input_folder_path = r"/excel_data/distances"
files = os.listdir(input_folder_path)
data_frames = []

# %% aggregate and unpack distances
for input_file in files:
    print(input_file)
    input_filepath = os.path.join(input_folder_path, input_file)
    single_df = pd.read_excel(input_filepath, sheet_name='surface_distances')
    # transposed_distances = single_df.T
    Row_list = []
    # Iterate over each row
    for index, rows in single_df.iterrows():
        # Create list for the current row
        my_list = rows.Distances
        # append the list to the final list
        Row_list.append(my_list)

    new_df = pd.DataFrame(data={
        'Patient': single_df['Patient'][1],
        'Lesion': single_df['Lesion'][1],
        'Distances': [Row_list]})

    data_frames.append(new_df)

data_aggregated = pd.concat(data_frames)
filepath_excel = "../plots/QAM_LTP_Distances.xlsx"
writer = pd.ExcelWriter(filepath_excel)
data_aggregated.to_excel(writer, sheet_name='radiomics', index=False, float_format='%.2f')
writer.save()


