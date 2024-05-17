import lazy_loader as lazy

__getattr__, __dir__, __all__ = lazy.attach(
    __name__,
    submodules=[
        "file_sequence",
        "sequence",
    ],
    submod_attrs={
        "abaqus": ["Abaqus"],
        "binary": ["Binary"],
        "cached_metadata": ["CachedMetadata"],
        "code_snippet": ["CodeSnippet"],
        "data_container": ["DataContainer"],
        "file": ["File", "load_file"],
        "file_sequence": ["FileSequence"],
        "group": ["Group", "load_groups"],
        "hdf5": ["HDF5"],
        "image": ["Image"],
        "matlab": ["MatlabData"],
        "meshio": ["Meshio"],
        "notebook": ["Notebook"],
        "pdf": ["PDF"],
        "pyvista_mesh": ["PyvistaMesh"],
        "symlink": ["SymLink"],
        "table": ["Table"],
        "text": ["Markdown", "Text"],
        "video": ["Video"],
        "xdmf": ["XDMF"],
        "xml": ["XML"],
    },
)
