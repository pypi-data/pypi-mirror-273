import h5py

from .. import viewers
from .file import File


class HDF5(File):
    """HDF5 loader"""

    supported_mime_types = ["application/x-hdf5"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.default_viewer = viewers.HDF5

    @File.loadable
    def datasets(self):
        return h5py.File(self.file_info.path)
