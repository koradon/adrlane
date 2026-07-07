from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("adrlane")
except PackageNotFoundError:  # pragma: no cover - editable/dev fallback
    __version__ = "0.0.0+dev"
