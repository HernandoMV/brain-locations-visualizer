"""
reads config file and creates variables
that can be accessed when this module is imported
and the function is called
"""

from pathlib import Path
import json


def config_parser(path_to_config_file):

    # define global variables
    global data_path, file_path
    global z_limits, y_limits
    global sl_list, n_images, rows, cols
    global id_1, id_2, color_1, color_2, color_other
    global atlas_path, cp_image_path

    # Open the JSON file and read the contents
    with open(path_to_config_file) as f:
        cdata = json.load(f)

    # Access the variables you want to import
    data_path = cdata["data_path"]
    file_path = cdata["locations_file"]

    # get the striatum limits
    z_limits = cdata["z_limits"]
    y_limits = cdata["y_limits"]

    # select number of slices to show, rows and cols
    sl_list = cdata["sl_list"]
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
