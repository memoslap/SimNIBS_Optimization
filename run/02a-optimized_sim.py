import numpy as np
import os
from os.path import isdir, join
import sys
from joblib.parallel import Parallel, delayed
import copy
import time
import pyvista as pv
import matplotlib
matplotlib.use('Agg', force=True)

root_dir = "/media/data03/hayekd/Memoslap/Sample1"   
path_to_utils = join(root_dir, "memoslap")
sys.path.append(path_to_utils)
import simnibs_memoslap_utils as smu
from simnibs.utils.file_finder import SubjectFiles

"""
Run focal montages in parallel using the memoslap utilities
"""

def run_wrap(m2m_dir, proj, delay, outpath, kwargs):
    # helper function for parallel running
    time.sleep(delay)
    pv.start_xvfb()
    subject_files = SubjectFiles(subpath=m2m_dir)
    outpath = join(outpath, proj.condition)
    sub_outpath = f"P{proj.proj_nr}_{proj.exp_cond}_{subject_files.subid}"
    print(sub_outpath)
    results_path = os.path.abspath(join(outpath, sub_outpath))
    if isdir(results_path):
        print(f"{results_path} already exists; skipping...")
        return {"m2m":m2m_dir, "proj":proj, "result":"DirExists"}
    #try:
    smu.run(m2m_dir, proj, outpath, **kwargs)
    # except:
    #     return {"m2m":m2m_dir, "proj":proj, "result":"RunFailed"}
    return {"m2m":m2m_dir, "proj":proj, "result":"Passed"}


path_to_utils = join(root_dir, "memoslap")
sys.path.append(path_to_utils)

# where the charm recos are
charm_dir = join(root_dir, "01-charm")
outpath = join(root_dir, "02-simulations", "02-optimized")

radius_surround = list(np.arange(40, 80, 5))
n_jobs = 45

# create project combinations
projs = []
for alg in ["euc", "res"]:
    for exp_condition in ["target"]:
        #for p_idx in [6]:
        for p_idx in np.arange(1,9):
            p = copy.copy(smu.projects[p_idx][exp_condition])
            p.radius = radius_surround
            p.condition = alg
            projs.append(p)
# cycle through subjects
queue = []
for subj in os.listdir(charm_dir):
    if f"m2m_{subj}" not in os.listdir(join(charm_dir, subj)):
        continue
    for proj in projs:
        queue.append((os.path.join(charm_dir, subj, f"m2m_{subj}"), proj))
kwargs = {"add_cerebellum":True, "map_to_fsavg":True}
delays = np.tile(np.arange(1, n_jobs+1)*2, int(np.ceil(len(queue)/n_jobs)))[:len(queue)]
result = Parallel(n_jobs=n_jobs)(delayed(run_wrap)(*q, d, outpath, kwargs) for q, d in zip(queue, delays))
