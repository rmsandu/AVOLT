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
    x = x.replace('[', '').replace(']', '').strip().split(',')
    return [float(v.strip()) for v in x if v not in ['', ' ']]


filepath_excel = r"C:\develop\AVOLT\AVOLT\plots\QAM_Distances_Radiomics_Chemo.xlsx"
df = pd.read_excel(filepath_excel)
df_vol = df.copy()
# create a valid list of numeric values
df.surface_distance = df.surface_distance.apply(fix_my_data)
# set index to LTP
df.set_index('ASR', inplace=True)
# pandas version 0.25 use explode to expand all lists
# update pandas if you're not on 0.25
df_sd = df.surface_distance.explode().rename_axis('ASR').reset_index(name='sd')
fig, ax = subplots(figsize=(10, 8))
sns.boxplot(x='ASR', y='sd', data=df_sd)
xticklabels = ['No', 'Yes']
xtickNames = setp(ax, xticklabels=xticklabels)
setp(xtickNames, fontsize=18, color='black')
ylabel('Quantitative ablation margin (QAM) [mm]', fontsize=18, color='black')
plt.xlabel('ASR (ablation site recurrence) at 6 months follow-up', fontsize=16, color='black')
ax.tick_params(colors='black')
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.show()
fig.savefig(r'C:\Users\Raluca Sandu\Dropbox\Phd Theses\Raluca\Figures\QAM_clinical_cases\asr_ltp_distances.png', dpi=600)

#%% TUMOR
fig2, ax2 = subplots(figsize=(10, 8))
sns.boxplot(x='ASR', y='mesh_volume_tumor', data=df_vol,  palette="colorblind")
xticklabels = ['No', 'Yes']
xtickNames = setp(ax2, xticklabels=xticklabels)
setp(xtickNames, fontsize=18, color='black')
ylabel('Tumor Volume [ml]', fontsize=18, color='black')
plt.xlabel('ASR (ablation site recurrence) at 6 months follow-up', fontsize=16, color='black')
ax2.tick_params(colors='black')
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
ax2.set_ylim([-1, 10])
plt.show()
fig2.savefig("asr_ltp_tumor_volume.png", dpi=600)

#%% ABLATION
fig3, ax3 = subplots(figsize=(12, 10))
sns.boxplot(x='ASR', y='mesh_volume_ablation', data=df_vol,  palette="pastel")
xticklabels = ['No', 'Yes']
xtickNames = setp(ax3, xticklabels=xticklabels)
setp(xtickNames, fontsize=18, color='black')
ylabel('Ablation Volume [ml]', fontsize=18, color='black')
plt.xlabel('ASR (ablation site recurrence) at 6 months follow-up', fontsize=16, color='black')
ax3.tick_params(colors='black')
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
#ax3.set_ylim([-1, 10])
plt.show()
fig3.savefig("asr_ltp_ablation_volume.png", dpi=600)
