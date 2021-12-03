# -*- coding: utf-8 -*-
"""
@author: Raluca Sandu
"""
import os
import time

import matplotlib
import matplotlib.pyplot as plt
from AVOLT.graphing import graphing

matplotlib.use('Agg')
import pandas as pd
import seaborn as sns
from scipy import stats
import numpy as np


def connected_mev_miv(df_radiomics):
    """
    Plots ablation volumes.
    :param df_radiomics: DataFrame containing tabular radiomics features
    :param ablation_vol_interpolated_brochure:  column-like interpolated ablation volume from the brochure
    :return: Plot, saved as a PNG image
    """

    df = pd.DataFrame()
    df['PAV'] = df_radiomics['Predicted_Ablation_Volume']
    df['EAV'] = df_radiomics['mesh_volume_ablation']
    df['MEV'] = df_radiomics['OuterEllipsoidVolume']
    df['MIV'] = df_radiomics['InnerEllipsoidVolume']
    # discard cases where the outer ellipsoid is greater than  200 ml  and where the inner ellipsoid is greater than the ablation volume
    df.loc[df['MEV'] > 200] = np.nan
    df.loc[df['MIV'] > df["EAV"], 'MIV'] = np.nan
    # plot scatter plots on the same y axis then connect them with a vertical line
    fig, ax = plt.subplots()
    MIV = np.asarray(df['MIV'])
    MEV = np.asarray(df['MEV'])
    PAV = np.asarray(df['PAV'])
    EAV = np.asarray(df['EAV'])
    x = np.asarray([i for i in range(1, len(MEV) + 1)])
    ax.scatter(x, MIV, marker='o', color='green', label='Maximum Inscribed Ellipsoid')
    ax.scatter(x, EAV, marker='o', color='orange', label='Effective Ablation Volume')
    ax.scatter(x, PAV, marker='o', color='blue', label='Predicted Ablation Volume')
    ax.scatter(x, MEV, marker='o', color='red', label='Minimum Enclosing Ellipsoid')
    plt.legend(loc='upper left')
    plt.ylabel('Volume [ml]')

    for i in np.arange(0, len(x)):
        x1, x2 = x[i], x[i]
        y1, y2 = MIV[i], MEV[i]
        plt.plot([x1, x2], [y1, y2], 'k-')

    # plt.ylim([-1, 150])
    # labels = np.round(np.asarray(df['PAV']))
    # plt.xticks(x, labels, rotation=45, fontsize=24, color='white')
    figpath = os.path.join("figures", "PAV_EAV_MIV_MEV_ellipsoids")
    graphing.save(figpath, width=12, height=12, ext=["png"], close=True, tight=True, dpi=600)

    # df.dropna(inplace=True)
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.boxplot(data=df, palette="viridis")
    plt.ylabel('Volume [ml]')
    fig.show()
    # b.set_xlabel(fontsize=20)
    # plt.ylim([])
    # plt.grid()
    figpath = os.path.join("figures", "PAV_EAV_MIV_MEV_ellipsoids_boxplots")
    graphing.save(figpath, width=12, height=12, ext=["png"], close=True, tight=True, dpi=600)


def plot_mev_miv(df_radiomics):
    """
    Plot a 3-subplot of pav vs eav, subcapsular and chemo
    :param df_radiomics:
    :return:
    """
    font = {'family': 'DejaVu Sans',
            'size': 18}
    matplotlib.rc('font', **font)

    df = pd.DataFrame()
    df['PAV'] = df_radiomics['Predicted_Ablation_Volume']
    df['EAV'] = df_radiomics['mesh_volume_ablation']
    df['Energy (kJ)'] = df_radiomics['Energy [kj]']
    df['MWA Systems'] = df_radiomics['Device_name']
    df['MIV'] = df_radiomics['InnerEllipsoidVolume']
    df['MEV'] = df_radiomics['OuterEllipsoidVolume']
    df.loc[df['MIV'] > df["EAV"], 'MIV'] = np.nan
    df['MEV-MIV'] = df['MEV'] - df['MIV']
    df['R(EAV:PAV)'] = df['EAV'] / df['PAV']

    fig, ax = plt.subplots(figsize=(12, 12))
    sns.distplot(df['Energy (kJ)'], hist_kws={"ec": 'black', "align": "mid"},
                 axlabel='Energy', ax=ax)
    timestr = time.strftime("%H%M%S-%Y%m%d")
    figpath = os.path.join("figures", 'Energy_distribution_' + timestr + '.png')
    plt.savefig(figpath, bbox_inches='tight', dpi=300)
    plt.close()
    # drop outer volumes larger than 150 because they are probably erroneous
    # drop the rows where MIV > MEV
    # since the minimum inscribed ellipsoid (MIV) should always be smaller than the maximum enclosing ellipsoid (MEV)
    df = df[df['MEV-MIV'] >= 0]
    min_val = int(min(df['MEV-MIV']))
    max_val = int(max(df['MEV-MIV']))
    print('Min Val Mev-Miv:', min_val)
    print('Max Val Mev-Miv:', max_val)
    print('nr of samples for mev-miv:', len(df))

    # %% histogram MEV-MIV
    fig, ax = plt.subplots(figsize=(12, 12))
    sns.distplot(df['MEV-MIV'], color=sns.xkcd_rgb["reddish"], hist_kws={"ec": 'black', "align": "mid"},
                 axlabel='Distribution of Ablation Volume Irregularity (MEV-MIV) (mL)', ax=ax)

    timestr = time.strftime("%H%M%S-%Y%m%d")
    figpath = os.path.join("figures", 'MEV-MIV_distribution_' + timestr + '.png')
    plt.savefig(figpath, bbox_inches='tight', dpi=300)
    plt.close()

    fig1, ax1 = plt.subplots(figsize=(12, 12))
    sns.distplot(df['MEV'], color=sns.xkcd_rgb["reddish"], hist_kws={"ec": 'black'},
                 axlabel='MEV', ax=ax1)
    timestr = time.strftime("%H%M%S-%Y%m%d")
    figpath = os.path.join("figures", 'MEV_distribution_' + timestr + '.png')
    plt.savefig(figpath, bbox_inches='tight', dpi=300)
    plt.close()

    fig1, ax2 = plt.subplots(figsize=(12, 12))
    sns.distplot(df['MIV'], color=sns.xkcd_rgb["reddish"], hist_kws={"ec": 'black'},
                 axlabel='MIV', ax=ax2)
    timestr = time.strftime("%H%M%S-%Y%m%d")
    figpath = os.path.join("figures", 'MIV_distribution_' + timestr + '.png')
    plt.savefig(figpath, dpi=300)
    plt.close()

    fig1, ax3 = plt.subplots(figsize=(12, 12))
    sns.distplot(df['EAV'], color=sns.xkcd_rgb["reddish"], hist_kws={"ec": 'black'},
                 axlabel='EAV', ax=ax3)
    timestr = time.strftime("%H%M%S-%Y%m%d")
    figpath = os.path.join("figures", 'EAV_distribution_' + timestr + '.png')
    plt.savefig(figpath, dpi=300)
    plt.close()

    fig1, ax4 = plt.subplots(figsize=(12, 12))
    sns.distplot(df['PAV'], color=sns.xkcd_rgb["reddish"], hist_kws={"ec": 'black'},
                 axlabel='PAV', ax=ax4)
    timestr = time.strftime("%H%M%S-%Y%m%d")
    figpath = os.path.join("figures", 'PAV_distribution_' + timestr + '.png')
    plt.savefig(figpath, dpi=300)
    plt.close()

    # %%   R (EAV:PAV) on y-axis and MEV-MIV on the x-axis
    fig1, ax5 = plt.subplots(figsize=(12, 12))
    slope, intercept, r_square, p_value, std_err = stats.linregress(df['R(EAV:PAV)'], df['MEV-MIV'])
    print('p-val mev miv energy:', p_value)
    print()
    p = sns.regplot(y="R(EAV:PAV)", x="MEV-MIV", data=df, scatter_kws={"s": 100, "alpha": 0.5},
                    color=sns.xkcd_rgb["reddish"],
                    line_kws={'label': r'$r = {0:.2f}$'.format(r_square)}, ax=ax5)
    plt.xlabel('MEV-MIV (mL)')
    plt.legend()

    timestr = time.strftime("%H%M%S-%Y%m%d")
    figpath = os.path.join("figures", 'Ratio_EAV-PAV_MEV-MIV_difference_' + timestr)
    plt.savefig(figpath, dpi=300, bbox_inches='tight')
    plt.close()
