from scipy.io import loadmat
import os
import pandas as pd
import re
from os.path import join
import pickle
import numpy as np

"""
this script goes through each directory within data_dir, grabs the data
out of the summary_metrics.mat file, and puts them into a pandas dataframe,
which allows easy plotting with python later. because this is for radial
montages, it needs to get both closest and optimal algorithms
"""
root_dir = "/media/data03/hayekd/Memoslap/Sample1"
data_dir = join(root_dir, "02-simulations", "02-optimized")

failed_dirs = []
# set up the dataframe variables
df_vars = ["Project", "Condition", "Subject", "Radii", "Mags_med",
           "Mags_sq", "Focs", "Phi", "Algo", "Center_X", "Center_Y", "Center_Z"
df_dict = {x:[] for x in df_vars}

for algo in ["euc", "res"]:
    algo_dir = join(data_dir, algo)
    files = os.listdir(algo_dir)
    for this_dir in files:
        re_rd = re.match("(.*)_(.*)_(\d*)", this_dir)
        if not re_rd:
            continue
        project, cond, subj = re_rd.groups()
        print(f"{project} {subj} {cond}")
        # load the data
        file_path = join(algo_dir, this_dir)
        try:
            with open(join(file_path, "simnibs_memoslap_results.pkl"), "rb") as f:
                results = pickle.load(f)
        except:
            continue
        mat = results[5]

        # put the data into the dataframe dictionary
        df_dict["Project"].append(project)
        df_dict["Subject"].append(subj)
        df_dict["Condition"].append(cond)
        df_dict["Algo"].append(algo)
        df_dict["Radii"].append(mat["radius"])
        df_dict["Mags_med"].append(mat["roi_median"]["E_magn"])
        df_dict["Mags_sq"].append(mat["roi_squared"]["E_magn"])
        df_dict["Focs"].append(mat["focality"]["E_magn"])
        df_dict["Phi"].append(results[0]["phi"])

df = pd.DataFrame.from_dict(df_dict)        
df.to_pickle(join(root_dir, "03-output", "02-optimized", "csvs", f"optimized_sample1.pickle"))
df.to_csv(os.path.join(root_dir, "03-output","02-optimized", "csvs", f"optimized_sample1.csv"))
    
mags_med = np.vstack(df["Mags_med"].values)
mags_sq = np.vstack(df["Mags_sq"].values)
focs = np.vstack(df["Focs"].values)
        
for idx in range(mags_med.shape[1]):
    df[f"Mags_med{idx+1}"] = mags_med[:, idx]
for idx in range(mags_sq.shape[1]):
    df[f"Mags_sq{idx+1}"] = mags_sq[:, idx]
for idx in range(focs.shape[1]):
    df[f"Foc{idx+1}"] = focs[:, idx]
        
df.to_excel(join(root_dir, "03-output", "02-optimized", "csvs", "optimized_sample1.xlsx"))
