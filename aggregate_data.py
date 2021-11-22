import pandas as pd


if __name__ == '__main__':
    input_files = snakemake.input
    output_file = snakemake.output[0]
    print('input files', input_files)
    df = pd.DataFrame(columns=['Patient', 'Lesion', 'InnerEllipsoidVolume',
                               'OuterEllipsoidVolume',
                               'center_of_mass_x_ablation',
                               'center_of_mass_y_ablation',
                               'center_of_mass_z_ablation',
                               'center_of_mass_index_x_ablation',
                               'center_of_mass_index_y_ablation',
                               'center_of_mass_index_z_ablation',
                               'elongation_ablation',
                               'sphericity_ablation',
                               'mesh_volume_ablation',
                               'volume_feature_ablation',
                               'diameter3D_ablation',
                               'diameter2D_slice_ablation',
                               'diameter2D_col_ablation',
                               'diameter2D_row_ablation',
                               'major_axis_length_ablation',
                               'least_axis_length_ablation',
                               'minor_axis_length_ablation',
                               'center_of_mass_x_tumor',
                               'center_of_mass_y_tumor',
                               'center_of_mass_z_tumor',
                               'center_of_mass_index_x_tumor',
                               'center_of_mass_index_y_tumor',
                               'center_of_mass_index_z_tumor',
                               'elongation_tumor',
                               'sphericity_tumor',
                               'mesh_volume_tumor',
                               'volume_feature_tumor',
                               'diameter3D_tumor',
                               'diameter2D_slice_tumor',
                               'diameter2D_col_tumor',
                               'diameter2D_row_tumor',
                               'major_axis_length_tumor',
                               'least_axis_length_tumor',
                               'minor_axis_length_tumor'])

    data_frames = []

    for input_file in input_files:
        print(input_file)
        df = pd.read_excel(input_file, sheet_name='radiomics')
        data_frames.append(df)

    data_aggregated = pd.concat(data_frames)
    data_aggregated.to_excel(output_file, sheet_name='radiomics', index=False)
