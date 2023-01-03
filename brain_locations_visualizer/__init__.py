from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("brain-locations-visualizer")
except PackageNotFoundError:
    # package is not installed
    pass
