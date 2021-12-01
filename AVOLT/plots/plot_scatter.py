# -*- coding: utf-8 -*-
"""
@author: Raluca Sandu
"""

import os
import time
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from AVOLT.utils import subplots_pav_eav_scatter
from AVOLT.utils import graphing
from AVOLT.utils import mev_miv_scatter


# # %% PLOT BOXPLOTS
# plot_boxplots_volumes(ablation_vol_interpolated_brochure, ablation_vol_measured,
#                                                flag_subcapsular=False)


def edit_save_plot(ax=None, p=None, flag_hue=None, xlabel='PAV', ylabel='EAV', device='',
                   r_1=None, r_2=None,
                   label_1=None, label_2=None,
                   ratio_flag=False):
    """

    :param ax:
    :param p:
    :param flag_hue:
    :param ylabel:
    :param device:
    :param r_1:
    :param r_2:
    :param label_1:
    :param label_2:
    :return:
    """
    fontsize = 20
    if flag_hue in ['vessels', 'subcapsular', 'chemotherapy', 'Tumor_Vol']:
        ax = p.axes[0, 0]
        ax.legend(fontsize=fontsize, title_fontsize=fontsize, title=device, loc='upper left')
        leg = ax.get_legend()
        L_labels = leg.get_texts()
        label_line_1 = r'$R^2:{0:.2f}$'.format(r_1)
        label_line_2 = r'$R^2:{0:.2f}$'.format(r_2)
        L_labels[0].set_text(label_line_1)
        L_labels[1].set_text(label_line_2)
        L_labels[2].set_text(label_1)
        L_labels[3].set_text(label_2)
    else:
        ax.legend(fontsize=fontsize, title_fontsize=fontsize, title=device, loc='upper right')
        # ax.legend(fontsize=fontsize,  loc='upper right')

    if ratio_flag is False:
        plt.xlim([0, 100])
        plt.ylim([0, 100])

    plt.xlabel(xlabel, fontsize=fontsize)
    plt.ylabel(ylabel, fontsize=fontsize)
    timestr = time.strftime("%H%M%S-%Y%m%d")
    figpath = os.path.join("figures", device + '__EAV_parametrized_PAV_groups_' + str(flag_hue) + '-' + timestr)
    graphing.save(figpath, width=12, height=12, ext=["png"], close=True, tight=True, dpi=600)


def plot_scatter_group_var_chemo(df_radiomics, ratio_flag=False):
    """

    :param df_radiomics:
    :param ratio_flag:
    :return:
    """
    df_radiomics.loc[df_radiomics.no_chemo_cycle > 0, 'no_chemo_cycle'] = 'Yes'
    df_radiomics.loc[df_radiomics.no_chemo_cycle == 0, 'no_chemo_cycle'] = 'No'
    # create new pandas DataFrame for easier plotting
    df = pd.DataFrame()
    df['PAV'] = df_radiomics['Predicted_Ablation_Volume']
    df['EAV'] = df_radiomics['Ablation Volume [ml]']
    df['Energy (kJ)'] = df_radiomics['Energy [kj]']
    df['Chemotherapy'] = df_radiomics['no_chemo_cycle']
    df['R(EAV:PAV)'] = df['EAV'] / df['PAV']
    df.dropna(inplace=True)
    print('Nr Samples used:', str(len(df)))
    label_2 = 'Chemotherapy: No'
    label_3 = 'Chemotherapy: Yes'
    chemo_false = df[df['Chemotherapy'] == 'No']
    chemo_true = df[df['Chemotherapy'] == 'Yes']
    if ratio_flag is True:
        p = sns.lmplot(y="R(EAV:PAV)", x="Energy (kJ)", hue="Chemotherapy", data=df, markers=["s", "s"],
                       palette=['mediumvioletred', 'green'],
                       ci=None, scatter_kws={"s": 150, "alpha": 0.8}, line_kws={'label': 'red'},
                       legend=True, legend_out=False)
        x1 = chemo_false['Energy (kJ)']
        y1 = chemo_false['R(EAV:PAV)']
        x2 = chemo_true['Energy (kJ)']
        y2 = chemo_true['R(EAV:PAV)']
        slope, intercept, r_2, p_value, std_err = stats.linregress(x1, y1)
        slope, intercept, r_1, p_value, std_err = stats.linregress(x2, y2)
        edit_save_plot(p=p, flag_hue='chemotherapy', ylabel='R(EAV:PAV)', xlabel='Energy (kJ)',
                       r_1=r_1, r_2=r_2, label_1=label_2, label_2=label_3, ratio_flag=True)
    elif ratio_flag is False:
        p = sns.lmplot(y="EAV", x="PAV", hue="Chemotherapy", data=df, markers=["s", "s"],
                       palette=['mediumvioletred', "green"],
                       ci=None, scatter_kws={"s": 150, "alpha": 0.8}, line_kws={'label': 'red'},
                       legend=True, legend_out=False)
        x1 = chemo_false['PAV']
        y1 = chemo_false['EAV']
        x2 = chemo_true['PAV']
        y2 = chemo_true['EAV']
        slope, intercept, r_2, p_value, std_err = stats.linregress(x1, y1)
        slope, intercept, r_1, p_value, std_err = stats.linregress(x2, y2)
        edit_save_plot(p=p, flag_hue='chemotherapy', ylabel='Effective Ablation Treatment [ml]',
                       xlabel='Predicted Ablation Treatment [ml]',
                       r_1=r_1, r_2=r_2, label_1=label_2, label_2=label_3)


def plot_scatter_group_var_subcapsular(df_radiomics, ratio_flag=False):
    """

    :param df_radiomics:
    :param ablation_vol_interpolated_brochure:
    :param ratio_flag:
    :return:
    """
    df = pd.DataFrame()
    df['PAV'] = df_radiomics['Predicted_Ablation_Volume']
    df['EAV'] = df_radiomics['mesh_volume_ablation']
    df['Energy (kJ)'] = df_radiomics['Energy [kj]']
    df['Subcapsular'] = df_radiomics['Proximity_to_surface']
    df['R(EAV:PAV)'] = df['EAV'] / df['PAV']
    # df.dropna(inplace=True)
    print('Nr Samples used:', str(len(df)))
    label_1 = 'Deep Tumors'  # Non-subcapsular aka Subcapsular False
    label_2 = 'Subcapsular'
    subcapsular_false = df[df['Subcapsular'] == False]
    subcapsular_true = df[df['Subcapsular'] == True]

    if ratio_flag is True:
        p = sns.lmplot(y="R(EAV:PAV)", x="Energy (kJ)", hue="Subcapsular", data=df, markers=["*", "*"],
                       palette=['cornflowerblue', 'orange'],
                       ci=None, scatter_kws={"s": 150, "alpha": 0.8}, line_kws={'label': 'red'},
                       legend=True, legend_out=False)
        slope, intercept, r_1, p_value, std_err = stats.linregress(subcapsular_false['Energy (kJ)'],
                                                                   subcapsular_false['R(EAV:PAV)'])
        slope, intercept, r_2, p_value, std_err = stats.linregress(subcapsular_true['Energy (kJ)'],
                                                                   subcapsular_true['R(EAV:PAV)'])
        edit_save_plot(p=p, flag_hue='subcapsular', ylabel='R(EAV:PAV)', xlabel='Energy (kJ)',
                       r_1=r_1, r_2=r_2, label_2=label_1, label_3=label_2)
    else:
        p = sns.lmplot(y="EAV", x="PAV", hue="Subcapsular", data=df, markers=["*", "*"],
                       palette=['cornflowerblue', 'orange'],
                       ci=None, scatter_kws={"s": 150, "alpha": 0.8}, line_kws={'label': 'red'},
                       legend=True, legend_out=False)
        # first legend false
        varx = subcapsular_false["PAV"]
        vary = subcapsular_false["EAV"]
        mask = ~np.isnan(varx) & ~ np.isnan(vary)
        slope, intercept, r_1, p_value, std_err = stats.linregress(varx[mask],
                                                                   vary[mask])
        varx = subcapsular_true["EAV"]
        vary = subcapsular_true["PAV"]
        mask = ~np.isnan(varx) & ~ np.isnan(vary)
        slope, intercept, r_2, p_value, std_err = stats.linregress(varx[mask],
                                                                   vary[mask])
        edit_save_plot(ax=None, p=p, flag_hue='subcapsular', ylabel='Effective Ablation Volume [ml]',
                       xlabel='Predicted Ablation Volume [ml]',
                       r_1=r_1, r_2=r_2, label_1=label_1, label_2=label_2)


def plot_scatter_pav_eav(df_radiomics,
                         ratio_flag=False,
                         linear_regression=True):
    """

    :param df_radiomics:
    :param ratio_flag:
    :return:
    """
    df = pd.DataFrame()
    df['PAV'] = df_radiomics['Predicted_Ablation_Volume']
    df['EAV'] = df_radiomics['mesh_volume_ablation']
    df['Energy (kJ)'] = df_radiomics['Energy [kj]']
    df['MWA Systems'] = df_radiomics['Device_name']
    df['major_axis_length_ablation'] = df_radiomics['major_axis_length_ablation']
    # df.dropna(inplace=True)
    print('Nr Samples used for PAV vs EAV scatter plot:', str(len(df)))
    if ratio_flag is False:
        if linear_regression is True:
            # df.dropna(inplace=True)
            varx = df['PAV']
            vary = df['EAV']
            mask = ~np.isnan(varx) & ~np.isnan(vary)
            slope, intercept, r_square, p_value, std_err = stats.linregress(varx[mask], vary[mask])
            ax = sns.regplot(x="PAV", y="EAV", data=df, scatter_kws={"s": 150, "alpha": 0.8},
                             color=sns.xkcd_rgb["violet"],
                             line_kws={'label': r'$r={0:.2f}$'.format(r_square)})
        else:
            ax = sns.scatterplot(x="PAV", y="EAV", data=df, s=200, alpha=0.8,
                                 color=sns.xkcd_rgb["violet"],  hue='MWA Systems')

        edit_save_plot(ax=ax, ylabel="Effective Ablation Volume [ml]", xlabel="Predicted Ablation Volume [ml]")
    else:
        df['R(EAV:PAV)'] = df['EAV'] / df['PAV']
        varx = df['R(EAV:PAV)'] 
        vary = df['major_axis_length_ablation']
        mask = ~np.isnan(varx) & ~np.isnan(vary)
        slope, intercept, r_square, p_value, std_err = stats.linregress(varx[mask], vary[mask])
        print('p-value R(EAV:PAV) vs Energy (kj):', p_value)
        if linear_regression is True:
            ax = sns.regplot(y="major_axis_length_ablation", x="Energy (kJ)", data=df, color=sns.xkcd_rgb["cobalt"],
                             line_kws={'label': r'$ r = {0:.2f}$'.format(r_square)},
                             scatter_kws={"s": 150, "alpha": 0.8})
        else:
            ax = sns.scatterplot(x="R(EAV:PAV)", y="Energy (kJ)", data=df, scatter_kws={"s": 150, "alpha": 0.8},
                                 color=sns.xkcd_rgb["violet"], hue='MWA Systems')

        edit_save_plot(ax=ax, ylabel="Maximum ablation diameter [mm]", xlabel="Energy [kJ]", ratio_flag=True)


def write_descriptive_stats(df_radiomics_PAV_EAV, device_name):
    """

    :param df_radiomics_PAV_EAV:
    :return: Excel file with descriptive statistics
    """
    df = pd.DataFrame()
    df['PAV'] = df_radiomics_PAV_EAV['Predicted_Ablation_Volume']
    df['EAV'] = df_radiomics_PAV_EAV['mesh_volume_ablation']
    df['Tumor_Volume'] = df_radiomics_PAV_EAV['mesh_volume_tumor']
    df['Energy'] = df_radiomics_PAV_EAV['Energy [kj]']
    df['Inner_Ellipsoid_Volume'] = df_radiomics_PAV_EAV['InnerEllipsoidVolume']
    df['Outer_Ellipsoid_Volume'] = df_radiomics_PAV_EAV['OuterEllipsoidVolume']
    # # drop outer volumes larger than 150 because they are probably erroneous
    #df.loc[df['Outer_Ellipsoid_Volume'] > 150, 'Outer_Ellipsoid_Volume'] = np.nan
    df.loc[df['Inner_Ellipsoid_Volume'] > df["EAV"], 'Inner_Ellipsoid_Volume'] = np.nan
    df.loc[df['Outer_Ellipsoid_Volume'] > 200] = np.nan
    df['MEV-MIV'] = df['Outer_Ellipsoid_Volume'] - df['Inner_Ellipsoid_Volume']
    df['Elongation'] = df_radiomics_PAV_EAV['elongation_ablation']
    df['Sphericity'] = df_radiomics_PAV_EAV['sphericity_ablation']
    df['major_axis_ablation'] = df_radiomics_PAV_EAV['major_axis_length_ablation']
    df['major_axis_tumor'] = df_radiomics_PAV_EAV['major_axis_length_tumor']
    df_stats = df.describe()

    iqr = df_stats.loc['75%', :] - df_stats.loc['25%', :]
    iqr.name = 'IQR'
    medd = df.median().to_frame().T
    medd.rename({0: 'median'})
    # median.index.name = 'median'
    df_stats = df_stats.append(medd, ignore_index=False)
    df_stats.rename({0: 'median'})
    df_stats = df_stats.append(iqr)
    filepath_excel = device_name + '_Radiomics_MAVERRIC_Descriptive_Stats.xlsx'
    writer = pd.ExcelWriter(filepath_excel)
    df_stats.to_excel(writer, sheet_name='radiomics', index=True, float_format='%.2f')
    writer.save()


if __name__ == '__main__':
    df_radiomics = pd.read_excel(r"C:\develop\AVOLT\AVOLT\plots\QAM_Distances_Radiomics_Chemo - Copy.xlsx")
    # change the name of the device
    df_radiomics.loc[df_radiomics.Device_name == 'Angyodinamics (Acculis)', 'Device_name'] = 'Acculis'
    df_radiomics.loc[df_radiomics.Device_name == 'Covidien (Covidien MWA)', 'Device_name'] = 'Covidien'
    df_radiomics.loc[df_radiomics.Device_name == 'Amica (Probe)', 'Device_name'] = 'Amica'
    # select only those rows included in the PAV vs EAV Energy Manuscript
    df_radiomics_PAV_EAV = df_radiomics[df_radiomics['Inclusion_Energy_PAV_EAV'] == True]
    # df_radiomics_PAV_EAV = df_radiomics_PAV_EAV[df_radiomics_PAV_EAV['Device_name'] == 'Acculis']
    # df_radiomics_PAV_EAV = df_radiomics_PAV_EAV[df_radiomics_PAV_EAV['Inclusion_Margin_Analysis'] == 1]
    # df_radiomics_PAV_EAV = df_radiomics_PAV_EAV[df_radiomics_PAV_EAV['Proximity_to_surface'] == False]



    #%%  SCATTER PLOTS
    # set font
    font = {'family': 'DejaVu Sans',
             'size': 18}
    matplotlib.rc('font', **font)
    #
    # subplots_pav_eav_scatter.plot_subplots(df_radiomics_PAV_EAV)
    # plot_scatter_pav_eav(df_radiomics_PAV_EAV, ratio_flag=False, linear_regression=True)
    # plot_scatter_pav_eav(df_radiomics_PAV_EAV, ratio_flag=False, linear_regression=False)
    # plot_scatter_pav_eav(df_radiomics_PAV_EAV, ratio_flag=True, linear_regression=True)
    # plot_scatter_group_var_subcapsular(df_radiomics_PAV_EAV, ratio_flag=False)

    #%% boxplot
    df_boxplots = pd.DataFrame()
    df_boxplots["Predicted ablation volume (PAV)"] = df_radiomics_PAV_EAV["Predicted_Ablation_Volume"]
    df_boxplots["Effective ablation volume (EAV)"] = df_radiomics_PAV_EAV["mesh_volume_ablation"]
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.boxplot(data=df_boxplots, palette="cividis")
    # xticklabels = ['No', 'Yes']
    # xtickNames = plt.setp(ax, xticklabels=xticklabels)
    # plt.setp(xtickNames, fontsize=18, color='black')
    plt.ylabel('Ablation volume [ml]', fontsize=18, color='black')
    # plt.xlabel('ASR (ablation site recurrence) at 6 months follow-up', fontsize=16, color='black')
    ax.tick_params(colors='black')
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    # ax3.set_ylim([-1, 10])
    fig.savefig("pav_eav_volume_boxplots_all2.png", dpi=600)

    #%% Descriptive statistics
    df_acculis = df_radiomics_PAV_EAV[df_radiomics_PAV_EAV['Device_name'] == 'Acculis']
    df_amica = df_radiomics_PAV_EAV[df_radiomics_PAV_EAV['Device_name'] == 'Amica']
    df_covidien = df_radiomics_PAV_EAV[df_radiomics_PAV_EAV['Device_name'] == 'Covidien']
    write_descriptive_stats(df_radiomics_PAV_EAV, device_name='All')
    write_descriptive_stats(df_acculis, device_name='Acculis')
    write_descriptive_stats(df_amica, device_name='Amica')
    write_descriptive_stats(df_covidien, device_name='Covidien')

    #     # plot ellipsoid approximations
    #     # mev_miv_scatter.plot_mev_miv(df_radiomics_PAV_EAV)
    #     # connected_mev_miv(df_radiomics_PAV_EAV)
