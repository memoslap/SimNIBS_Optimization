import pandas as pd
import matplotlib.pyplot as plt
plt.ion()
import matplotlib.gridspec as gridspec
import seaborn as sns
import os
import numpy as np
from os.path import join
from scipy.stats import mode

import matplotlib
font = {'weight' : 'bold',
        'size'   : 18}
matplotlib.rc('font', **font)

root_dir = "/media/data03/hayekd/Memoslap/Sample1"
fig_dir = join(root_dir, "03-output", "02-optimized", "figures")
data_dir = join(root_dir, "03-output", "02-optimized")
df = pd.read_pickle(join(data_dir, "csvs", "optimized_sample1.pickle"))

projects = np.sort(df["Project"].unique())
inner = None
dot_size = 9

# v4: closest vs optimal
best_radii = {}
best_vals = {"Project":[], "Subject":[], "Algo":[], "Mags_med":[],
             "Mags_sq":[], "Focs":[]}
# get best radius for groups
for project in projects:
    best_radii[project] = {}
    proj_df = df.query(f"Project=='{project}'")
    for algo in ["euc", "res"]:
        algo_df = proj_df.query(f"Algo=='{algo}'")
        rads = np.stack(algo_df["Mags_med"].values)
        meds = np.median(rads, axis=0)
        error = meds - 0.21
        error[error<0] = np.inf
        rad_idx = np.argmin(error)
        radii = algo_df["Radii"].values[0]
        best_radius = radii[rad_idx]
        best_radii[project][algo] = best_radius

        best_radius = radii[rad_idx]
        best_radii[project][algo] = best_radius
        subjs = np.sort(algo_df["Subject"].unique())
        for subj in subjs:
            line = algo_df.query(f"Subject=='{subj}'")
            rad_idx = list(line["Radii"].values[0]).index(best_radius)
            best_vals["Project"].append(project)
            best_vals["Subject"].append(subj)
            best_vals["Algo"].append(algo)
            best_vals["Mags_med"].append(line["Mags_med"].values[0][rad_idx])
            best_vals["Mags_sq"].append(line["Mags_sq"].values[0][rad_idx])
            best_vals["Focs"].append(line["Focs"].values[0][rad_idx])
best_vals = pd.DataFrame.from_dict(best_vals)

for measure, title in zip(["Mags_med", "Mags_sq", "Focs"],
                          ["Median Magnitude", "Sq. Magnitude", "Focality"]):
    fig, ax = plt.subplots(figsize=(38.4, 8))

    # Violin plot
    sns.violinplot(data=best_vals, x="Project", y=measure, hue="Algo",
                   ax=ax, inner=None)  

    # Strip plot
    sns.stripplot(data=best_vals, x="Project", y=measure, hue="Algo",
                  ax=ax, dodge=True, color="black", legend=False, size=dot_size)  

    # Customize the plot
    if measure == "Mags_med":
        plt.axhline(0.21, linestyle="--", color="gray")
        ax.set_ylim(0, 0.7)
    if measure == "Focs":
        ax.set_ylim(0, 12000)
    ax.set_title(f"{title}: euc vs res - Sample 1", fontsize=24,
                 fontweight="bold")
    ax.set_xlabel("Project (euc/res best radius)", fontsize=24,
                  fontweight="bold")
    ax.set_ylabel(title, fontsize=24, fontweight="bold")
    ax.set_xticklabels([f"{k} ({v['euc']}/{v['res']})"
                        for k, v in best_radii.items()])

    # Plot box plot on top
    for project, pos in enumerate(ax.get_xticks()):
        data = best_vals[best_vals["Project"] == projects[project]]
        for algo, color in zip(["euc", "res"], ["white", "white"]):
            box_data = data[data["Algo"] == algo][measure]
            bp = plt.boxplot(box_data.values,
                             positions=[pos + (0.2 if algo == "euc" else -0.2)],
                             widths=0.2, patch_artist=True, showmeans=True,
                             meanprops={"marker":"o", "markerfacecolor":"white", "markeredgecolor":"black"},
                             boxprops=dict(facecolor="lightgrey", alpha=0.7),
                             medianprops=dict(color="black"),
                             manage_ticks=False,
                             zorder=3)  # Ensure boxplot is in front
            for element in ['boxes', 'whiskers', 'fliers', 'means', 'medians', 'caps']:
                plt.setp(bp[element], color=color)
                
    # Save figure
    plt.tight_layout()
    plt.savefig(join(fig_dir, f"{measure}_euc_v_res_violin_boxplot_sample1_newP3_0.21.pdf"))
    plt.savefig(join(fig_dir, f"{measure}_euc_v_res_violin_boxplot_sample1_newP3_0.21.jpg"))
    plt.savefig(join(fig_dir, f"{measure}_euc_v_res_violin_boxplot_sample1_newP3_0.21.eps"))

plt.show()
