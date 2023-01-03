"""
plot_fiber_tips_2D_striatum.py
==============================================================
generates two figures with the fiber tips in the striatum

1. Specify the parameters and files
-----------------------------------
1.1 Import required packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from PIL import Image
import json
import sys
    
def plot_fiber_tips_2D_striatum(config_file):
    # 1.2 Get the parameters by parsing the configuration file
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Open the JSON file and read the contents
    with open(config_file) as f:
        cdata = json.load(f)

    # Access the variables you want to import
    data_path = cdata["data_path"]
    file_path = cdata["locations_file"]

    # get the striatum limits
    z_limits = cdata["z_limits"]
    y_limits = cdata["y_limits"]

    # select number of slices to show, rows and cols
    n_images = cdata["n_images"]
    rows = cdata["rows"]
    cols = cdata["cols"]

    # get the identifier to separate mice
    id_1 = cdata["id_1"]
    id_2 = cdata["id_2"]

    # get colors for different identifiers
    color_1 = cdata["color_1"]
    color_2 = cdata["color_2"]
    color_other = cdata["color_other"]

    # atlas files paths
    atlas_path = Path(data_path) / Path(cdata["atlas_path"])
    cp_image_path = Path(data_path) / Path(cdata["cp_image_path"])

    # plot with a different marker the flat fibers and the tapered fibers (this is specified in the mouse name)
    ff_marker = '_'
    tf_marker = '|'

    # define the output directory as the parent of the config file
    parent = Path(config_file).parent

    # read the file of points
    coords = pd.read_csv(file_path, header=0)
    X = coords.x
    Y = coords.y
    Z = coords.z
    Animal_Name = coords.Mouse_name

    # select only the fibers used in the analysis
    # CAREFUL HERE WITH WHERE IS LEFT AND WHERE IS RIGHT!!
    # animals that are not included have a # in front of their name
    animal_mask = [not an.startswith('#') for an in Animal_Name]
    X = np.array(list(X[animal_mask])).astype(float)
    Y = np.array(list(Y[animal_mask])).astype(float)
    Z = np.array(list(Z[animal_mask])).astype(float)
    Animal_Name = np.array(list(Animal_Name[animal_mask]))


    ### This part decides which slices to show

    # Option 1: show images evenly:
    # read atlas get slice numbers
    atlas = Image.open(atlas_path)
    try:
        h,w,_ = np.shape(atlas)
    except:
        h,w = np.shape(atlas)
    
    # decide on the number of images
    step = int(np.floor((z_limits[1] - z_limits[0]) / n_images))
    sl_list = list(range(z_limits[0], z_limits[1], step))
    sl_list = sl_list[-n_images:]
    # hack
    # extreme tail focused:
    # sl_list = [150, 200, 240,
    #            265, 270, 275,
    #            280, 285, 290,
    #            295, 300, 305]

    sl_list = [150, 175, 200,
            225, 235, 245,
            255, 265, 275,
            285, 295, 305]

    # better coverage of NAc:
    # sl_list = [160, 175, 190,
    #            205, 235, 245,
    #            255, 265, 275,
    #            285, 295, 305]

    # Mirror all to the right hemisphere
    atlas_mid_point = w/2
    for i in range(len(Z)):
        if Z[i] < atlas_mid_point:
            dist_to_center = atlas_mid_point - Z[i]
            Z[i] = atlas_mid_point + dist_to_center

    # separate animals
    mask_1 = [x.startswith(id_1) for x in Animal_Name]
    mask_2 = [x.startswith(id_2) for x in Animal_Name]
    mask_other = np.logical_and([not e for e in mask_1],
                                [not e for e in mask_2])

    ff_mask = [x.endswith('_flat') for x in Animal_Name]
    tf_mask = [not x for x in ff_mask]

    # make the plot
    fig, ax = plt.subplots(1, 1, figsize=[10,10])
    # show striatum outline
    str_im = Image.open(cp_image_path)
    ax.imshow(str_im)
    # show where slices are taken from
    ax.vlines(sl_list, y_limits[0], y_limits[1],
            linestyles='dotted', color='grey', alpha=.3)
    # plot points
    for i in range(len(X)):
        if mask_1[i]:
            col = color_1
        if mask_2[i]:
            col = color_2
        if mask_other[i]:
            color_other
        if ff_mask[i]:
            mt = ff_marker
        if tf_mask[i]:
            mt = tf_marker
        ax.plot(X[i], Y[i], mt, color=col,
                alpha=.9, markersize=12, markeredgewidth=6)
    # ax.plot(X[mask_2], Y[mask_2], 'x', color=color_2,
    #         alpha=.8, markersize=10, markeredgewidth=4)
    # ax.plot(X[mask_other], Y[mask_other], 'x', color=color_other,
    #         alpha=.8, markersize=10, markeredgewidth=4)
    # add limits of striatum
    ax.set_ylim(bottom=y_limits[0], top=y_limits[1])
    ax.set_xlim(left=z_limits[0], right=z_limits[1])
    ax.set_aspect('equal', 'box')
    ax.invert_yaxis()
    # convert to mm
    a=ax.get_xticks().tolist()
    a= [25 * a[i] / 1000 for i in range(len(a))]
    ax.set_xticklabels(a, fontsize=18)
    a=ax.get_yticks().tolist()
    a= [25 * a[i] / 1000 for i in range(len(a))]
    ax.set_yticklabels(a, fontsize=18)
    ax.set_xlabel('ARA A-P axis (mm)', fontsize=22)
    ax.set_ylabel('ARA D-V axis (mm)', fontsize=22)

    # Hide the right and top spines
    ax.spines.right.set_visible(False)
    ax.spines.top.set_visible(False)
    plt.savefig(parent / 'sideview_plot.pdf',
                transparent=True, bbox_inches='tight')
    # plt.show(fig)

    # plot the fibers in the slices
    fig2, axs = plt.subplots(rows, cols, figsize=[cols * w/50, rows * h/50])
    axs = axs.ravel()
    for c,i in enumerate(sl_list):
        atlas.seek(i)
        axs[c].imshow(atlas)#, cmap='gray_r')
        axs[c].axis('off')
    # fig2.subplots_adjust(wspace=0, hspace=0)
    fig2.tight_layout()

    # plot the fibers
    for c,x in enumerate(X):
        # find the index of the slice that this point is closest to
        templist = [np.abs(b - x) for b in sl_list]
        idx = np.argmin(templist)
        if mask_1[c]:
            col = color_1
        if mask_2[c]:
            col = color_2
        if mask_other[c]:
            col = color_other
        if ff_mask[c]:
            mt = ff_marker
        if tf_mask[c]:
            mt = tf_marker
        axs[idx].plot(Z[c], Y[c],
                    marker=mt, color=col, alpha=.8,
                    markersize=15, markeredgewidth=5)
    plt.savefig(parent / 'slice_comp_plot.pdf',
                transparent=True, bbox_inches='tight')
    # plt.show(fig2)


if __name__ == '__main__':
    # check input
    if len(sys.argv) not in [1, 2]:
        sys.exit('Incorrect number of arguments, please run like this:\
            python plot_fiber_tips_2D_striatum.py optional:path_to_config_file')
    
    if len(sys.argv) == 2:
        # use the provided config file
        inpath = sys.argv[2]
        # run function
        plot_fiber_tips_2D_striatum(config_file=inpath)
    else:
        # use the default config file
        try:
            inpath = Path(__file__).parent / '../data/example_config.json'
        except NameError: # __file__ is not defined (for example when running in jupyter)
            inpath = Path('../data/example_config.json')
        plot_fiber_tips_2D_striatum(config_file=inpath)
