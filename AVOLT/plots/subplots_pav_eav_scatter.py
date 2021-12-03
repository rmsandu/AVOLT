# -*- coding: utf-8 -*-
"""
@author: Raluca Sandu
"""
import os
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from AVOLT.graphing import graphing as gh
from scipy import stats


def plot_subplots(df_radiomics):
    """
    Plot a 3-subplot of pav vs eav, subcapsular and chemo
    :param df_radiomics:
    :return: plot fo png file
    """
    # Set up the matplotlib figure
    f, axes = plt.subplots(1, 3, figsize=(20, 20))
    fontsize = 10
    fontsize_legend = 9
    df = pd.DataFrame()
    df['PAV'] = df_radiomics['Predicted_Ablation_Volume']
    df['EAV'] = df_radiomics['mesh_volume_ablation']
    df['Energy (kJ)'] = df_radiomics['Energy [kj]']
    df['MWA Systems'] = df_radiomics['Device_name']
    df['Proximity_to_surface'] = df_radiomics['Proximity_to_surface']
    df['Chemotherapy'] = df_radiomics['chemo_before_ablation']
    df['Chemo_yes'] = df['EAV']
    df['Chemo_no'] = df['EAV']
    df['Subcapsular'] = df['EAV']
    df['Non-Subcapsular'] = df['EAV']
    df.loc[
        df.Proximity_to_surface == False, 'Subcapsular'] = np.nan  # only keep those with value true, ie subcapsular
    df.loc[df.Proximity_to_surface == True, 'Non-Subcapsular'] = np.nan
    df.loc[
        df.Chemotherapy == 'No', 'Chemo_yes'] = np.nan
    df.loc[df.Chemotherapy == 'Yes', 'Chemo_no'] = np.nan  # chemo no

    print('Nr Samples used:', str(len(df)))

    # %% 1st plot PAV vs EAV with lin regr
    varx = df['PAV']
    vary = df['EAV']
    mask = ~np.isnan(varx) & ~np.isnan(vary)
    slope, intercept, r_square, p_value, std_err = stats.linregress(varx[mask], vary[mask])
    print('slope value PAV vs. EAV:', slope)
    print('p-value PAV vs EAV:', p_value)
    sns.regplot(x="PAV", y="EAV", data=df, scatter_kws={"s": 11, "alpha": 0.6},
                color=sns.xkcd_rgb["violet"],
                line_kws={'label': r'$r:{0:.2f}$'.format(r_square)}, ax=axes[0])
    axes[0].legend(fontsize=fontsize_legend, loc='upper left')
    axes[0].set_ylabel('EAV [ml]', fontsize=fontsize)
    axes[0].set_xlabel('PAV [ml]', fontsize=fontsize)

    # %% Subcapsular 2nd plot
    subcapsular_false = df[df['Proximity_to_surface'] == False]
    subcapsular_true = df[df['Proximity_to_surface'] == True]
    varx = subcapsular_false['PAV']
    vary = subcapsular_false['EAV']
    mask = ~np.isnan(varx) & ~np.isnan(vary)
    slope, intercept, r_1, p_value, std_err = stats.linregress(varx[mask], vary[mask])
    varx = subcapsular_true['PAV']
    vary = subcapsular_true['EAV']
    mask = ~np.isnan(varx) & ~np.isnan(vary)
    slope, intercept, r_2, p_value, std_err = stats.linregress(varx[mask], vary[mask])

    # Wilcoxon paired signed rank test
    w, p = stats.wilcoxon(subcapsular_true['PAV'], subcapsular_true['EAV'])
    print('p-val wilcoxon subcapsular true:', p)
    w, p = stats.wilcoxon(subcapsular_false['PAV'], subcapsular_false['EAV'])
    print('p-val wilcoxon subcapsular false:', p)

    sns.regplot(y="Non-Subcapsular", x="PAV", data=df, scatter_kws={"s": 11, "alpha": 0.6},
                line_kws={'label': r'No: $r = {0:.2f}$'.format(r_1)},
                ax=axes[1])
    sns.regplot(y="Subcapsular", x="PAV", data=df, scatter_kws={"s": 11, "alpha": 0.6},
                color=sns.xkcd_rgb["orange"], line_kws={'label': r'Yes: $r = {0:.2f}$'.format(r_2)},
                ax=axes[1])
    axes[1].legend(fontsize=fontsize_legend, loc='best', title='Subcapsular', title_fontsize=fontsize_legend)
    axes[1].set_yticklabels([])
    axes[1].set_ylabel('')
    axes[1].set_xlabel('PAV [ml]', fontsize=fontsize)
    # axes[1].set_title('Predicted (PAV) vs Effective Ablation Volume (EAV) for all MWA Devices', fontsize=fontsize, pad=20)

    # %% Chemo 3rd plot
    chemo_false = df[df['Chemotherapy'] == 'No']
    chemo_true = df[df['Chemotherapy'] == 'Yes']
    varx = chemo_false['PAV']
    vary = chemo_false['EAV']
    mask = ~np.isnan(varx) & ~np.isnan(vary)
    slope, intercept, r_1, p_value, std_err = stats.linregress(varx[mask], vary[mask])
    varx = chemo_true['PAV']
    vary = chemo_true['EAV']
    mask = ~np.isnan(varx) & ~np.isnan(vary)
    slope, intercept, r_2, p_value, std_err = stats.linregress(varx[mask], vary[mask])
    w, p = stats.wilcoxon(chemo_true['PAV'], chemo_true['EAV'])
    print('p-val chemotherapy yes:', p)
    w, p = stats.wilcoxon(chemo_false['PAV'], chemo_false['EAV'])
    print('p-val chemotherapy no:', p)
    sns.regplot(y='Chemo_yes', x="PAV", data=df, scatter_kws={"s": 11, "alpha": 0.6}, color=sns.xkcd_rgb["teal green"],
                ax=axes[2], line_kws={'label': r'Yes: $r = {0:.2f}$'.format(r_2)})
    sns.regplot(y='Chemo_no', x="PAV", data=df, scatter_kws={"s": 11, "alpha": 0.6}, color=sns.xkcd_rgb["slate grey"],
                ax=axes[2], line_kws={'label': r'No: $r = {0:.2f}$'.format(r_1)})
    axes[2].legend(fontsize=fontsize_legend, loc='best', title='Chemotherapy', title_fontsize=fontsize_legend)
    axes[2].set_yticklabels([])
    axes[2].set_ylabel('')
    axes[2].set_xlabel('PAV [ml]', fontsize=fontsize)

    # add major title to subplot
    # f.suptitle('Predicted (PAV) vs Effective Ablation Volume (EAV) for 3 MWA Devices', fontsize=10)

    # set the axes limits and new ticks
    axes[2].set_xlim([0, 81])
    axes[1].set_xlim([0, 81])
    axes[0].set_xlim([0, 81])

    axes[2].set_ylim([0, 81])
    axes[1].set_ylim([0, 81])
    axes[0].set_ylim([0, 81])

    axes[0].xaxis.set_ticks(np.arange(0, 81, 20))
    axes[1].xaxis.set_ticks(np.arange(0, 81, 20))
    axes[2].xaxis.set_ticks(np.arange(0, 81, 20))

    plt.subplots_adjust(wspace=0.1)

    # set the fontsize of the ticks of the subplots
    for ax in axes:
        ax.set(adjustable='box', aspect='equal')
        ax.tick_params(axis='both', which='major', labelsize=fontsize)

    # save the figure
    timestr = time.strftime("%H%M%S-%Y%m%d")
    figpath = os.path.join("figures", 'All_MWA_Devices_PAVEAV_Subcapsular_Chemo_' + timestr)
    plt.show()
    gh.save(figpath, ext=["png"], width=12, height=12, close=True, tight=True, dpi=600)
