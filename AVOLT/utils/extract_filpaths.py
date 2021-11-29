# -*- coding: utf-8 -*-
"""
@author: Raluca Sandu
"""
import os
import pandas as pd
rootdir = r"D:\MAVERRIC_2021"

list_all_ct_series = []
for subdir, dirs, files in os.walk(rootdir):
    tumor_source = None
    ablation_source = None
    tumor = None
    ablation = None
    for idx, val in enumerate(files):
        patient_id = subdir.split("\\")[-2]
        lesion = subdir.split("\\")[-1]
        if "Tumor_Source.nii.gz" in val:
            tumor_source = os.path.join(subdir, val)
        elif "Tumor.nii.gz" in val:
            tumor = os.path.join(subdir, val)
        if "Ablation_Source.nii.gz" in val:
            ablation_source = os.path.join(subdir, val)
        elif "Ablation.nii.gz" in val:
            ablation = os.path.join(subdir, val)
        excel_filepath = patient_id + '_lesion' + lesion + '.xlsx'
        if (tumor and ablation_source and tumor_source and ablation) is not None:
            dict_series_folder = {
                "Patient": patient_id,
                "Lesion": lesion,
                "tumor": tumor,
                "ablation": ablation,
                "tumour_source": tumor_source,
                "ablation_source": ablation_source,
                "output_radiomics": excel_filepath,
            }
            list_all_ct_series.append(dict_series_folder)

df_paths_mapping = pd.DataFrame(list_all_ct_series)
writer = pd.ExcelWriter("filepaths_maverric.xlsx")
df_paths_mapping.to_excel(writer, sheet_name='paths', index=False, float_format='%.4f')
writer.save()
