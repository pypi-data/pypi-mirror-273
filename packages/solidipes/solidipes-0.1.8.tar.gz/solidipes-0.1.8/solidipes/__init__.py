"""Computational solid mechanics package for loading and visualizing files"""

import lazy_loader as lazy

__getattr__, __dir__, __all__ = lazy.attach(
    __name__,
    [
        "loaders",
        "reports",
        "scanners",
        "uploaders",
        "utils",
        "viewers",
    ],
    submod_attrs={
        "loaders": ["load_file"],
    },
)

__version__ = "0.1.8"
