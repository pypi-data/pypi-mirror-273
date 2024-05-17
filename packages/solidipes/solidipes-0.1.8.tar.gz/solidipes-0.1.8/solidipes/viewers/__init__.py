import lazy_loader as lazy

__getattr__, __dir__, __all__ = lazy.attach(
    __name__,
    submod_attrs={
        "binary": ["Binary"],
        "code_snippet": ["Code"],
        "hdf5": ["HDF5"],
        "image": ["Image"],
        "matlab": ["MatlabData"],
        "notebook": ["Notebook"],
        "pdf": ["PDF"],
        "pyvista_plotter": ["PyvistaPlotter"],
        "symlink": ["SymLink"],
        "table": ["Table"],
        "text": ["MarkdownViewer", "Text"],
        "video": ["Video"],
        "viewer": ["Viewer"],
        "xdmf": ["XDMF"],
        "xml": ["XML"],
    },
)
