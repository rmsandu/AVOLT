# -*- coding: utf-8 -*-
"""
@author: Raluca Sandu
"""
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import griddata
from sklearn import linear_model

import utils.graphing as gh


def interpolation_fct(df_ablation, df_radiomics, device_name, fontsize=24, flag=None,
                      flag_energy_axis=False, flag_lin_regr=False):
    """
    :param df_ablation:
    :param df_radiomics:
    :param device_name:
    :param fontsize:
    :param flag:
    :param flag_energy_axis:
    :return:
    """
    # perform interpolation as a function of  power and time (multivariate interpolation)
    points_power = np.asarray(df_ablation['Power']).reshape((len(df_ablation), 1))
    points_time = np.asarray(df_ablation['Time_Duration_Applied']).reshape((len(df_ablation), 1))
    power_and_time_brochure = np.hstack((points_power, points_time))
    ablation_vol_brochure = np.asarray(df_ablation['Predicted Ablation Volume (ml)']).reshape((len(df_ablation), 1))
    df_radiomics.dropna(subset=['Power', 'Time_Duration_Applied'], inplace=True)
    grid_x = df_radiomics['Power'].to_numpy()
    grid_y = df_radiomics['Time_Duration_Applied'].to_numpy()
    grid_x = np.array(pd.to_numeric(grid_x, errors='coerce'))
    grid_y = np.array(pd.to_numeric(grid_y, errors='coerce'))
    grid_x = grid_x.reshape(len(grid_x), 1)
    grid_y = grid_y.reshape(len(grid_y), 1)
    power_and_time_effective = np.asarray(np.hstack((grid_x, grid_y)))

    ablation_vol_interpolated_brochure = griddata(power_and_time_brochure, ablation_vol_brochure,
                                                  power_and_time_effective, method='linear')
    ablation_vol_interpolated_brochure = ablation_vol_interpolated_brochure.reshape(len(df_radiomics), )
    ablation_vol_measured = np.asarray(df_radiomics['Ablation Volume [ml]']).reshape(len(df_radiomics), )

    # %% PLOT BOXPLOTS
    # boxplots_PAV_EAV.plot_boxplots_volumes(ablation_vol_interpolated_brochure, ablation_vol_measured,
    #                              flag_subcapsular='all', device_name=device_name)
    # %% PLOT SCATTER PLOTS
    fig, ax = plt.subplots()
    if flag == 'Tumour Volume [ml]':
        size_values = np.asarray(df_radiomics['Tumour Volume [ml]']).reshape(len(df_radiomics), )
        df = pd.DataFrame(data=dict(x=ablation_vol_interpolated_brochure, y=ablation_vol_measured, sizes=size_values))
        df.dropna(inplace=True)
        bins = np.arange(start=0, stop=30, step=5)
        grouped = df.groupby(np.digitize(df.sizes, bins))
        sizes = [150 * (i + 1.) for i in range(6)]
        labels = ['0-5', '5-10', '10-15', '15-20', '20-25', '25-30']

        nr_samples = len(df)
        for i, (name, group) in enumerate(grouped):
            plt.scatter(group.x, group.y, s=sizes[i], alpha=0.5, label=labels[name - 1])

        legend1 = ax.legend(labelspacing=1, borderpad=0.75, title='Tumor Volume [ml]',
                            handletextpad=1.5, loc='upper right', fontsize=fontsize - 2, title_fontsize=fontsize - 2)
        ax.add_artist(legend1)
        ax.tick_params(axis='y', labelsize=fontsize)
        ax.tick_params(axis='x', labelsize=fontsize)
        plt.tick_params(labelsize=fontsize, color='k')

    elif flag == 'No. chemo cycles':
        size_values = np.asarray(df_radiomics['no_chemo_cycle']).reshape(len(df_radiomics), )
        df = pd.DataFrame()
        df['x'] = ablation_vol_interpolated_brochure
        df['y'] = ablation_vol_measured
        df['sizes'] = size_values
        df.dropna(inplace=True)
        nr_samples = len(df)
        bins = np.arange(start=0, stop=12, step=4)
        print(np.digitize(df.sizes, bins, right=True))
        grouped = df.groupby(np.digitize(df.sizes, bins, right=True))
        sizes = [150 * (i + 1.) for i in range(4)]
        labels = ['0', '1-4', '5-8', '9-12']
        for i, (name, group) in enumerate(grouped):
            plt.scatter(group.x, group.y, s=sizes[i], alpha=0.5, label=labels[name])
        legend1 = ax.legend(labelspacing=1, borderpad=0.75, title='Chemotherapy Cycles',
                            handletextpad=1.5, loc='upper right', fontsize=fontsize - 2,
                            device_name_fontsize=fontsize - 2)
        ax.add_artist(legend1)
    else:
        df = pd.DataFrame(data=dict(x=ablation_vol_interpolated_brochure, y=ablation_vol_measured))
        df.dropna(inplace=True)
        sc = plt.scatter(df.x, df.y, color='steelblue', marker='o', s=150, alpha=0.7)
        nr_samples = len(df)
    plt.ylabel('Effective Ablation Volume (mL)', fontsize=fontsize)
    if flag_energy_axis is False:
        plt.xlabel('Predicted Ablation Volume Brochure (mL)', fontsize=fontsize)
    plt.ylim([0, 60])
    plt.xlim([0, 60])
    if flag_lin_regr is True:
        # get the data ready for linear regression
        X = np.asarray(df.x).reshape(len(df.x), 1)
        Y = np.asarray(df.y).reshape(len(df.y), 1)
        regr = linear_model.LinearRegression()
        regr.fit(X, Y)
        SS_tot = np.sum((Y - np.mean(Y)) ** 2)
        residuals = Y - regr.predict(X)
        SS_res = np.sum(residuals ** 2)
        r_squared = 1 - (SS_res / SS_tot)
        correlation_coef = np.corrcoef(X[:, 0], Y[:, 0])[0, 1]
        label_r2 = r'$R^2:{0:.2f}$'.format(r_squared)
        label_r = r'$r: {0:.2f}$'.format(correlation_coef)
        print('R square', label_r2)
        print('r', label_r)
        ax.tick_params(axis='y', labelsize=fontsize)
        ax.tick_params(axis='x', labelsize=fontsize)
        plt.tick_params(labelsize=fontsize, color='k')
        reg = plt.plot(X, regr.predict(X), color='black', linewidth=2.5, label='Linear Regression')
        plt.plot([], [], ' ', label=label_r)
        plt.plot([], [], ' ', label=label_r2)
        plt.legend(fontsize=fontsize, loc='upper right', labelspacing=1)
    if flag is not None:
        # these are matplotlib.patch.Patch properties
        props = dict(boxstyle='round', facecolor='white', edgecolor='gray')
        textstr = device_name + ' (n = ' + str(nr_samples) + ' )'
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=20, verticalalignment='top', bbox=props)
        figpathHist = os.path.join("figures",
                                   device_name + flag + '_ablation_vol_interpolated')
    else:
        props = dict(boxstyle='round', facecolor='white', edgecolor='gray')
        textstr = device_name + ' (n = ' + str(nr_samples) + ' )'
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=20, verticalalignment='top', bbox=props)
        plt.legend(fontsize=fontsize, loc='upper right', labelspacing=1)
        figpathHist = os.path.join("figures", device_name + '_ablation_vol_interpolated')

    gh.save(figpathHist, width=12, height=12, ext=["png"], close=True, tight=True, dpi=600)

    return ablation_vol_interpolated_brochure


if __name__ == '__main__':
    df_ablation = pd.read_excel(r"C:\develop\segmentation-eval\Ellipsoid_Brochure_Info.xlsx")
    df_radiomics = pd.read_excel(r"C:\develop\segmentation-eval\Radiomics_Acculis_MAVERRIC_22012020.xlsx")
    # select subcapsular values
    # Proximity_to_surface = False --> deep lesions
    # Proximity to surface = True --> subcapsular
    # df_radiomics = df_radiomics[df_radiomics['Proximity_to_surface'] == True]
    df_acculis = df_ablation[df_ablation['Device_name'] == 'Angyodinamics (Acculis)']
    df_acculis.reset_index(inplace=True)
    df_radiomics_acculis = df_radiomics[df_radiomics['Device_name'] == 'Angyodinamics (Acculis)']
    df_radiomics_acculis = df_radiomics_acculis[(df_radiomics_acculis['Comments'].isnull())]
    df_radiomics_acculis.reset_index(inplace=True)

    # flag_options : 1. flag == 'No. chemo cycles' 2. flag == 'Tumour Volume [ml]'
    interpolation_fct(df_acculis, df_radiomics_acculis, 'Acculis MWA System', flag='Tumour Volume [ml]',
                      flag_energy_axis=False, flag_lin_regr=False)
