# brain-locations-visualizer

Uses point locations, in 3D coordinates of the Allen Brain Atlas, to create different visualisations for these locations:
<p align="middle">
  <img src="docs/imgs/main.png" width=550>
</p>

### Installation

Clone this repo

In your terminal, navigate to the folder where you cloned it and run:
```
pip install -e .
```

Download supporting data (e.g. atlas) from [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7501966.svg)](https://doi.org/10.5281/zenodo.7501966)

Put it inside the data folder.

### Usage

All the scripts work with a text file that specifies the coordinates of the points you want to display (e.g. tip of a fiber).
This file looks like the one in the example:
```
data/example_locations.txt
```

TODO: explain the way to get these points in Fiji

Edit the main path variable in the configuration file to the data folder
```
data/example_config.json
```

#### Create visualization of coronal sections and a side view of the striatum

