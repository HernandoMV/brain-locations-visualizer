import matplotlib.pyplot as plt
from PIL import Image
import numpy as np


def generate_side_figure(
    config_parser,
    sl_list,
    X,
    Y,
    mask_1,
    mask_2,
    mask_other,
    ff_mask,
    tf_mask,
    ff_marker,
    tf_marker,
    parent,
):
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
    plt.savefig(
        parent / "sideview_plot.pdf", transparent=True, bbox_inches="tight"
    )
    # plt.show(fig)


def generate_coronal_figure(
    config_parser,
    sl_list,
    w,
    h,
    atlas,
    X,
    Y,
    Z,
    mask_1,
    mask_2,
    mask_other,
    ff_mask,
    tf_mask,
    ff_marker,
    tf_marker,
    parent,
):
    """
    things

    :param config_parser: _description_
    :type config_parser: _type_
    :param sl_list: _description_
    :type sl_list: _type_
    :param w: _description_
    :type w: _type_
    :param h: _description_
    :type h: _type_
    :param atlas: _description_
    :type atlas: _type_
    :param X: _description_
    :type X: _type_
    :param Y: _description_
    :type Y: _type_
    :param Z: _description_
    :type Z: _type_
    :param mask_1: _description_
    :type mask_1: _type_
    :param mask_2: _description_
    :type mask_2: _type_
    :param mask_other: _description_
    :type mask_other: _type_
    :param ff_mask: _description_
    :type ff_mask: _type_
    :param tf_mask: _description_
    :type tf_mask: _type_
    :param ff_marker: _description_
    :type ff_marker: _type_
    :param tf_marker: _description_
    :type tf_marker: _type_
    :param parent: _description_
    :type parent: _type_
    """
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
    plt.savefig(
        parent / "slice_comp_plot.pdf", transparent=True, bbox_inches="tight"
    )
    # plt.show(fig2)
