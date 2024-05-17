from .. import viewers
from .file import File


class MatlabData(File):
    """Matlab .mat file"""

    supported_mime_types = ["application/x-matlab-data"]
    supported_extensions = ["mat"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.default_viewer = viewers.MatlabData

    @File.loadable
    def arrays(self):
        import scipy.io

        mat = scipy.io.loadmat(self.file_info.path)
        return mat
