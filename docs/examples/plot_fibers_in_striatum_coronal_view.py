"""
plot_fibers_in_striatum_coronal_view.py
=======================================
generates a coronal view of the striatum with the fiber tips

1. Import required packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import pandas as pd
import numpy as np
from pathlib import Path
from PIL import Image
from brain_locations_visualizer import config_parser
from brain_locations_visualizer.plotting_functions import generate_coronal_figure

#%%
# 2. Get the configuration file and define variables
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# use the default config file for the documentation
config_file = Path("config_for_documentation.json")

# variables are assigned in the config_parser function
config_parser.config_parser(config_file)

#%%
# plot with a different marker the flat fibers and the tapered fibers
# (this is specified in the mouse name)
ff_marker = "_"
tf_marker = "|"

#%%
# define the output directory as the parent of the config file
parent = Path(config_file).parent

#%%
# read the file of points
coords = pd.read_csv(config_parser.file_path, header=0)
X = coords.x
Y = coords.y
Z = coords.z
Animal_Name = coords.Mouse_name

#%%
# select only the fibers used in the analysis
# CAREFUL HERE WITH WHERE IS LEFT AND WHERE IS RIGHT!!
# animals that are not included have a # in front of their name
animal_mask = [not an.startswith("#") for an in Animal_Name]
X = np.array(list(X[animal_mask])).astype(float)
Y = np.array(list(Y[animal_mask])).astype(float)
Z = np.array(list(Z[animal_mask])).astype(float)
Animal_Name = np.array(list(Animal_Name[animal_mask]))

#%%
# **2.1 This part decides which slices to show**
 
# read atlas and get its dimensions
atlas = Image.open(config_parser.atlas_path)
try:
    h, w, _ = np.shape(atlas)
except Exception:
    h, w = np.shape(atlas)

#%%
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
    sl_list = sl_list[-config_parser.n_images :]

else:
    sl_list = config_parser.sl_list

#%%
# Mirror all to the right hemisphere (optional)
atlas_mid_point = w / 2
for i in range(len(Z)):
    if Z[i] < atlas_mid_point:
        dist_to_center = atlas_mid_point - Z[i]
        Z[i] = atlas_mid_point + dist_to_center

#%%
# define masks for the different animals and fiber types
mask_1 = [x.startswith(config_parser.id_1) for x in Animal_Name]
mask_2 = [x.startswith(config_parser.id_2) for x in Animal_Name]
mask_other = np.logical_and(
    [not e for e in mask_1], [not e for e in mask_2]
)

ff_mask = [x.endswith("_flat") for x in Animal_Name]
tf_mask = [not x for x in ff_mask]

#%%
# 2. Generate the figure
# ~~~~~~~~~~~~~~~~~~~~~~
generate_coronal_figure(
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
)

