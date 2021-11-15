# -*- coding: utf-8 -*-
"""
Created on Nov 14 2021

@author: Raluca Sandu
"""

import argparse
import sys
from datetime import date
from AVOLT.extract_radiomics import RadiomicsMetrics
import numpy as np
import pandas as pd


from AVOLT.utils.niftireader import load_image

np.set_printoptions(suppress=True, precision=4)
today = date.today()


def get_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--tumor", required=True, help="path to the tumor segmentation")
    ap.add_argument("-a", "--ablation", required=True, help="path to the ablation segmentation")
    ap.add_argument("-tct", "--tumor-source", required=True, help="path to the tumor CT source")
    ap.add_argument("-act", "--ablation-source", required=True, help="path to the ablation CT source")
    ap.add_argument("-om", "--output-radiomics", required=True, help="output radiomics (xlsx)")
    ap.add_argument("-p", "--patient-id", required=False, help="patient id from study")
    ap.add_argument("-i", "--lesion-id", required=False, help="lesion id")
    ap.add_argument("-d", "--ablation-date", required=False, help="ablation date from study")
    args = vars(ap.parse_args())
    return args


if __name__ == '__main__':

    args = get_args()
    tumor_file = args['tumor']
    ablation_file = args['ablation']
    tumor_source = args['tumor_source']
    ablation_source = args['ablation_source']
    patient_id = args['patient_id']
    lesion_id = args['lesion_id']
    ablation_date = args['ablation_date']
    output_file_radiomics = args['output_radiomics']
    # check whether the input has been provided for all vars if not give some random values
    if patient_id is None:
        patient_id = 'Test'
    if lesion_id is None:
        lesion_id = 1
    if ablation_date is None:
        ablation_date = today.strftime("%d-%m-%Y")

    # read the ct source imgs
    tumor_source_nii, tumor_source_np = load_image(tumor_source)
    ablation_source_nii, ablation_source_np = load_image(ablation_source)

    # check if there is actually a tumor/ablation segmentation in the files
    tumor_nii, tumor_np = load_image(tumor_file)
    has_tumor_segmented = np.sum(tumor_np.astype(np.uint8)) > 0
    if has_tumor_segmented is False:
        print('No tumor segmentation mask found in the file provided...program exiting')
        sys.exit()
    ablation_nii, ablation_np = load_image(ablation_file)
    has_ablation_segmented = np.sum(ablation_np.astype(np.uint8)) > 0

    if has_ablation_segmented is False:
        print('No ablation segmentation mask found in the file provided...program exiting')
        sys.exit()

    # extract the spacing from the ablation file
    pixdim = ablation_source_nii.header['pixdim']
    spacing = (pixdim[1], pixdim[2], pixdim[3])

    # %% Get Radiomics Metrics (shape and intensity)
    # ABLATION
    ablation_radiomics_metrics = RadiomicsMetrics(ablation_source, ablation_file)
    if ablation_radiomics_metrics.error_flag is False:
        df_ablation_metrics_1set = ablation_radiomics_metrics.get_axis_metrics_df()
        new_columns_name = df_ablation_metrics_1set.columns + '_ablation'
        df_ablation_metrics_1set.columns = new_columns_name
    else:
        df_ablation_metrics_1set = None
    # TUMOR
    tumor_radiomics_metrics = RadiomicsMetrics(tumor_source, tumor_file)
    if tumor_radiomics_metrics.error_flag is False:
        df_tumor_metrics_1set = tumor_radiomics_metrics.get_axis_metrics_df()
        new_columns_name = df_tumor_metrics_1set.columns + '_tumor'
        df_tumor_metrics_1set.columns = new_columns_name
    else:
        df_tumor_metrics_1set = None

    patient_df = pd.DataFrame(data={
            'Patient': [patient_id] * len(df_tumor_metrics_1set),
            'Lesion': [lesion_id] * len(df_tumor_metrics_1set)})

    df_metrics = pd.concat([patient_df, df_ablation_metrics_1set, df_tumor_metrics_1set], axis=1)
    writer = pd.ExcelWriter(output_file_radiomics)
    df_metrics.to_excel(writer, sheet_name='radiomics', index=False, float_format='%.4f')

    writer.save()

