# -*- coding: utf-8 -*-
import importlib.metadata

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "croudtech-python-aws-app-config"
    __version__ = importlib.metadata.distribution(dist_name).version
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"
finally:
    del importlib.metadata