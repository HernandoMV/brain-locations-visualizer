import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from brainrender import Scene
from brainrender import settings
from brainrender.actors import Points


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


def generate_3D_figure(config_parser, X, Y, Z, animal_name, parent):
    """
    Print fiber locations in 3D
    """

    settings.SHOW_AXES = False
    settings.WHOLE_SCREEN = False

    # Radius of points
    rad = 50

    # alpha of points
    alpha = 0.6

    top_half_camera = {
        "pos": (2561, -19083, -5807),
        "viewup": (-1, 0, 0),
        "clippingRange": (12258, 36810),
        "focalPoint": (6314, 4543, -2712),
        "distance": 24122,
    }

    top_camera = {
        "pos": (1814, -32863, -5453),
        "viewup": (-1, 0, 0),
        "clippingRange": (27457, 49150),
        "focalPoint": (6767, 4440, -5946),
        "distance": 37634,
    }

    back_camera = {
        "pos": (32023, -388, -5767),
        "viewup": (0, -1, 0),
        "clippingRange": (17887, 40832),
        "focalPoint": (6732, 4204, -5674),
        "distance": 25705,
    }

    zoom_camera = {
        "pos": (24178, 1210, -3760),
        "viewup": (0, -1, 0),
        "clippingRange": (9250, 33210),
        "focalPoint": (6633, 3937, -2468),
        "distance": 17803,
    }

    plane_center = [8655.15806343, 4271.67187907, 5632.09744594]

    # Plot all together:
    scene = Scene(inset=False, title="", screenshots_folder=parent)
    region = scene.add_brain_region("CP", alpha=0.2, color="gray")
    region2 = scene.add_brain_region("ACB", alpha=0.2, color="gray")
    region3 = scene.add_brain_region("FS", alpha=0.2, color="gray")

    # import the custom mesh from AU1 TODO
    # scene.add(own_mesh, color="tomato")
    fname = "_" + str(rad)

    pts = np.array([[x, y, z] for x, y, z in zip(X, Y, Z)])
    for i in range(len(animal_name)):
        if animal_name[i].startswith(config_parser.id_1):
            scene.add(
                Points(
                    np.array([pts[i]]),
                    name="fiber_tips",
                    colors=config_parser.color_1,
                    radius=rad,
                    alpha=alpha,
                )
            )
        if animal_name[i].startswith(config_parser.id_2):
            scene.add(
                Points(
                    np.array([pts[i]]),
                    name="fiber_tips",
                    colors=config_parser.color_2,
                    radius=rad,
                    alpha=alpha,
                )
            )

    # scene.content
    # top views
    scene.render(camera=top_half_camera, zoom=1.2, interactive=True)
    scene.screenshot(name="top_half_view_all" + fname + ".png")

    scene.render(camera=top_camera, zoom=1.2, interactive=False)
    scene.screenshot(name="top_view_all" + fname + ".png")

    # back view
    scene.render(camera=back_camera, zoom=1.2, interactive=False)
    plane = scene.atlas.get_plane(pos=plane_center, norm=(-1, 0, 0))
    scene.slice(plane)
    scene.screenshot(name="back_view_all" + fname + ".png")

    # zoom view
    plane = scene.atlas.get_plane(pos=plane_center, norm=(-1, 0, 0))
    scene.render(camera=zoom_camera, zoom=1.2, interactive=False)
    scene.screenshot(name="zoom_view_all" + fname + ".png")

    # close
    scene.close()
