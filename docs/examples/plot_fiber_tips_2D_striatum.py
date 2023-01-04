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
from brain_locations_visualizer import config_parser


def plot_fiber_tips_2D_striatum(config_file):
    # 1.2 Get the parameters by parsing the configuration file
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # variables are assigned in the config_parser function
    config_parser.config_parser(config_file)

    # plot with a different marker the flat fibers and the tapered fibers
    # (this is specified in the mouse name)
    ff_marker = "_"
    tf_marker = "|"

    # define the output directory as the parent of the config file
    # parent = Path(config_file).parent

    # read the file of points
    coords = pd.read_csv(config_parser.file_path, header=0)
    X = coords.x
    Y = coords.y
    Z = coords.z
    Animal_Name = coords.Mouse_name

    # select only the fibers used in the analysis
    # CAREFUL HERE WITH WHERE IS LEFT AND WHERE IS RIGHT!!
    # animals that are not included have a # in front of their name
    animal_mask = [not an.startswith("#") for an in Animal_Name]
    X = np.array(list(X[animal_mask])).astype(float)
    Y = np.array(list(Y[animal_mask])).astype(float)
    Z = np.array(list(Z[animal_mask])).astype(float)
    Animal_Name = np.array(list(Animal_Name[animal_mask]))

    # This part decides which slices to show
    # read atlas and get its dimensions
    atlas = Image.open(config_parser.atlas_path)
    try:
        h, w, _ = np.shape(atlas)
    except Exception:
        h, w = np.shape(atlas)

    # show images evenly if the precise slices are not specified
    # in the config file
    if config_parser.sl_list == []:
        step = int(
            np.floor(
                (config_parser.z_limits[1] - config_parser.z_limits[0])
                / config_parser.n_images
            )
        )
        sl_list = list(
            range(config_parser.z_limits[0], config_parser.z_limits[1], step)
        )
        sl_list = sl_list[-config_parser.n_images:]

    else:
        sl_list = config_parser.sl_list

    # Mirror all to the right hemisphere
    atlas_mid_point = w / 2
    for i in range(len(Z)):
        if Z[i] < atlas_mid_point:
            dist_to_center = atlas_mid_point - Z[i]
            Z[i] = atlas_mid_point + dist_to_center

    # separate animals
    mask_1 = [x.startswith(config_parser.id_1) for x in Animal_Name]
    mask_2 = [x.startswith(config_parser.id_2) for x in Animal_Name]
    mask_other = np.logical_and(
        [not e for e in mask_1], [not e for e in mask_2]
    )

    ff_mask = [x.endswith("_flat") for x in Animal_Name]
    tf_mask = [not x for x in ff_mask]

    # make the plot
    fig, ax = plt.subplots(1, 1, figsize=[10, 10])
    # show striatum outline
    str_im = Image.open(config_parser.cp_image_path)
    ax.imshow(str_im)
    # show where slices are taken from
    ax.vlines(
        sl_list,
        config_parser.y_limits[0],
        config_parser.y_limits[1],
        linestyles="dotted",
        color="grey",
        alpha=0.3,
    )
    # plot points
    for i in range(len(X)):
        if mask_1[i]:
            col = config_parser.color_1
        if mask_2[i]:
            col = config_parser.color_2
        if mask_other[i]:
            config_parser.color_other
        if ff_mask[i]:
            mt = ff_marker
        if tf_mask[i]:
            mt = tf_marker
        ax.plot(
            X[i],
            Y[i],
            mt,
            color=col,
            alpha=0.9,
            markersize=12,
            markeredgewidth=6,
        )
    # ax.plot(X[mask_2], Y[mask_2], 'x', color=color_2,
    #         alpha=.8, markersize=10, markeredgewidth=4)
    # ax.plot(X[mask_other], Y[mask_other], 'x', color=color_other,
    #         alpha=.8, markersize=10, markeredgewidth=4)
    # add limits of striatum
    ax.set_ylim(
        bottom=config_parser.y_limits[0], top=config_parser.y_limits[1]
    )
    ax.set_xlim(
        left=config_parser.z_limits[0], right=config_parser.z_limits[1]
    )
    ax.set_aspect("equal", "box")
    ax.invert_yaxis()
    # convert to mm
    a = ax.get_xticks().tolist()
    a = [25 * a[i] / 1000 for i in range(len(a))]
    ax.set_xticklabels(a, fontsize=18)
    a = ax.get_yticks().tolist()
    a = [25 * a[i] / 1000 for i in range(len(a))]
    ax.set_yticklabels(a, fontsize=18)
    ax.set_xlabel("ARA A-P axis (mm)", fontsize=22)
    ax.set_ylabel("ARA D-V axis (mm)", fontsize=22)

    # Hide the right and top spines
    ax.spines.right.set_visible(False)
    ax.spines.top.set_visible(False)
    # plt.savefig(
    #     parent / "sideview_plot.pdf", transparent=True, bbox_inches="tight"
    # )
    # plt.show(fig)

    # plot the fibers in the slices
    fig2, axs = plt.subplots(
        config_parser.rows,
        config_parser.cols,
        figsize=[config_parser.cols * w / 50, config_parser.rows * h / 50],
    )
    axs = axs.ravel()
    for c, i in enumerate(sl_list):
        atlas.seek(i)
        axs[c].imshow(atlas)  # , cmap='gray_r')
        axs[c].axis("off")
    # fig2.subplots_adjust(wspace=0, hspace=0)
    fig2.tight_layout()

    # plot the fibers
    for c, x in enumerate(X):
        # find the index of the slice that this point is closest to
        templist = [np.abs(b - x) for b in sl_list]
        idx = np.argmin(templist)
        if mask_1[c]:
            col = config_parser.color_1
        if mask_2[c]:
            col = config_parser.color_2
        if mask_other[c]:
            col = config_parser.color_other
        if ff_mask[c]:
            mt = ff_marker
        if tf_mask[c]:
            mt = tf_marker
        axs[idx].plot(
            Z[c],
            Y[c],
            marker=mt,
            color=col,
            alpha=0.8,
            markersize=15,
            markeredgewidth=5,
        )
    # plt.savefig(
    #     parent / "slice_comp_plot.pdf", transparent=True, bbox_inches="tight"
    # )
    # plt.show(fig2)


if __name__ == "__main__":
    # use the default config file for the documentation
    inpath = Path("config_for_documentation.json")
    plot_fiber_tips_2D_striatum(config_file=inpath)
