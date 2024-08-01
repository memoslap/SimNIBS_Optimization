import matplotlib.pyplot as plt
import os
from os.path import join, isdir
import re
import sys
import pyvista as pv
pv.start_xvfb()

root_dir = "/media/data03/hayekd/Memoslap/Sample1"
data_dir = join(root_dir, "02-simulations", "02-optimized", "res")
charm_dir = join(root_dir, "01-charm")
fig_dir = join(root_dir, "04-mass_reports", "02-optimized")

path_to_utils = join(root_dir, "memoslap")
sys.path.append(path_to_utils)
import simnibs_memoslap_utils as smu
from simnibs_memoslap_utils.reporting import (_mag_plot, _elec_plot_geo,
                                              _pvmesh_from_skin_geo,
                                              _elpos_from_geo, _roi_plot)

cam_dist = 400
condition = "target"
subjs = os.listdir(charm_dir)
sub_per_page = 2

fig_count = 0
fig_sub_idx = 0
for subj_idx, subj in enumerate(subjs):
    subj = subj[-3:]
    if fig_sub_idx == 0:
        fig, axes = plt.subplots(3*sub_per_page, 8, figsize=(38.4, 21.6))
    for proj in range(1,9):
        subj_dir = f"P{proj}_{condition}_{subj}"
        if subj_dir not in os.listdir(data_dir):
            print(f"skipping {subj_dir}")
            continue
        mesh_path = join(data_dir, subj_dir)
        radius = int(smu.projects[int(proj)][condition].radius[0])

        # plot electrodes
        skin_file = f"P{proj}_{condition}_{subj}_skin.geo"
        if skin_file not in os.listdir(mesh_path):
            continue
        elpos_file = f"P{proj}_{condition}_{subj}_{radius}_elpos.geo"
        mesh = _pvmesh_from_skin_geo(join(mesh_path, skin_file))
        points = _elpos_from_geo(join(mesh_path, elpos_file))
        elec_img, foc = _elec_plot_geo(mesh, points, return_foc=True,
                                       cam_dist=cam_dist)
        axes[3*fig_sub_idx, proj-1].imshow(elec_img)
        axes[3*fig_sub_idx, proj-1].axis("off")

        # load mesh
        mesh = pv.read(join(mesh_path,
                            f"P{proj}_{condition}_{subj}_{radius}.msh"))
        # plot fields
        mag_image = _mag_plot(mesh, cam_dist=cam_dist*0.7, foc=foc)
        axes[3*fig_sub_idx+1, proj-1].imshow(mag_image)
        axes[3*fig_sub_idx+1, proj-1].axis("off")

        # plot roi
        roi_image = _roi_plot(mesh, foc=foc, cam_dist=cam_dist*.7)
        axes[3*fig_sub_idx+2, proj-1].imshow(roi_image)
        axes[3*fig_sub_idx+2, proj-1].axis("off")

        # text
        trans = axes[sub_per_page*fig_sub_idx, proj-1].transAxes
        axes[sub_per_page*fig_sub_idx, proj-1].text(0.05, 0.8, f"P{proj}",
                                                  fontsize=36,
                                                  transform=trans)
    trans = axes[3*fig_sub_idx, 0].transAxes
    axes[3*fig_sub_idx, 0].text(0.95, 0.8, subj,
                                           fontsize=36,
                                           transform=trans,
                                           horizontalalignment="right" )
    fig_sub_idx += 1
    if fig_sub_idx == sub_per_page or (subj_idx==(len(subjs)-1)):
        plt.tight_layout()
        plt.savefig(join(fig_dir,
                         f"res_{condition}_{fig_count}_magn.pdf"))
        plt.close()
        fig_count += 1
        fig_sub_idx = 0
