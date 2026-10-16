"""meteoscope : exploration of meteorological data."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("meteoscope")
except PackageNotFoundError:  # exécution hors installation (rare)
    __version__ = "0.0.0+source"
