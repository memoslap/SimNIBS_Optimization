import pandas as pd
import matplotlib.pyplot as plt
plt.ion()
import matplotlib.gridspec as gridspec
import seaborn as sns
import os
import numpy as np
from os.path import join

import matplotlib
font = {'weight' : 'bold',
        'size'   : 18}
matplotlib.rc('font', **font)

root_dir = "/media/data03/hayekd/Memoslap/Sample1"
fig_dir = join(root_dir, "03-output", "02-optimized", "figures")
data_dir = join(root_dir, "03-output", "02-optimized")

best_rads_dict = {"Version":[], "Project":[], "Radius":[]}
dot_size = 9

subplots = (2, 4)
# compare closest and optimal with across subject averages
df = pd.read_pickle(join(data_dir, "csvs", "optimized_sample1.pickle"))
projects = np.sort(df["Project"].unique())
mag_m_fig, mag_m_axes = plt.subplots(subplots[0], subplots[1],
                                     figsize=(38.4, 21.6))
plt.suptitle("Magnitude_Median: Version 4 - euc vs res - Sample1")
mag_s_fig, mag_s_axes = plt.subplots(subplots[0], subplots[1],
                                     figsize=(38.4, 21.6))
plt.suptitle("Magnitude_Sq: Version 4 - euc vs res - Sample1")
foc_fig, foc_axes = plt.subplots(subplots[0], subplots[1],
                                figsize=(38.4, 21.6))
plt.suptitle("Focality: Version 4 - euc vs res")
mag_m_axes = [ax for axe in mag_m_axes for ax in axe]
mag_s_axes = [ax for axe in mag_s_axes for ax in axe]
foc_axes = [ax for axe in foc_axes for ax in axe]

for proj_idx, project in enumerate(projects):
    this_df = df.query(f"Project=='{project}'")
    # build a new df in a format where this can be easily plotted
    df_dict = {"Subject":[], "Radius":[], "Magnitude_med":[],
               "Magnitude_sq":[], "Focality":[], "Algo":[]}
    radii = this_df.iloc[0]["Radii"]
    for row_idx, row in this_df.iterrows():
        for rad_idx, radius in enumerate(radii):
            df_dict["Subject"].append(row["Subject"])
            df_dict["Radius"].append(radius)
            df_dict["Magnitude_med"].append(row["Mags_med"][rad_idx])
            df_dict["Magnitude_sq"].append(row["Mags_sq"][rad_idx])
            df_dict["Focality"].append(row["Focs"][rad_idx])
            df_dict["Algo"].append(row["Algo"])
    temp_df = pd.DataFrame.from_dict(df_dict)

    sns.lineplot(data=temp_df, x="Radius", y="Magnitude_med", hue="Algo",
                 ax=mag_m_axes[proj_idx], palette=["r", "g"],
                 hue_order=["res", "euc"], estimator='median')
    sns.lineplot(data=temp_df, x="Radius", y="Magnitude_sq", hue="Algo",
                 ax=mag_s_axes[proj_idx], palette=["r", "g"],
                 hue_order=["res", "euc"], estimator='median')
    sns.lineplot(data=temp_df, x="Radius", y="Focality", hue="Algo",
                 ax=foc_axes[proj_idx] , palette=["r", "g"],
                 hue_order=["res", "euc"], estimator='median')
    mag_m_axes[proj_idx].set_title(project)
    mag_m_axes[proj_idx].set_ylim([.05, .5])
    mag_m_axes[proj_idx].axhline(0.21, color="gray", linestyle="--")
    mag_s_axes[proj_idx].set_title(project)
    mag_s_axes[proj_idx].set_ylim([0, 600])
    foc_axes[proj_idx].set_ylim([1000, 7500])
    foc_axes[proj_idx].set_title(project)
    
mag_m_fig.savefig(join(fig_dir, "mag_m_euc_v_res_sample1_newP3_0.21.pdf"))
mag_s_fig.savefig(join(fig_dir, "mag_s_euc_v_res_sample1_newP3_0.21.pdf"))
foc_fig.savefig(join(fig_dir, "foc_euc_v_res_sample1_newP3_0.21.pdf"))

mag_m_fig.savefig(join(fig_dir, "mag_m_euc_v_res_sample1_newP3_0.21.jpg"))
mag_s_fig.savefig(join(fig_dir, "mag_s_euc_v_res_sample1_newP3_0.21.jpg"))
foc_fig.savefig(join(fig_dir, "foc_euc_v_res_sample1_newP3_0.21.jpg"))

mag_m_fig.savefig(join(fig_dir, "mag_m_euc_v_res_sample1_newP3.eps"))
mag_s_fig.savefig(join(fig_dir, "mag_s_euc_v_res_sample1_newP3.eps"))
foc_fig.savefig(join(fig_dir, "foc_euc_v_res_sample1_newP3.eps"))

