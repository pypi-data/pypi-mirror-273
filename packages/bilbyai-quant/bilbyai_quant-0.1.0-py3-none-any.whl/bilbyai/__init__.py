from importlib import metadata

try:
    __version__ = metadata.version(__package__)  # type: ignore
except metadata.PackageNotFoundError:
    __version__ = ""
