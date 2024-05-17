from .. import viewers
from .file import File


class Meshio(File):
    """File loaded with meshio"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.default_viewer = viewers.PyvistaPlotter

    @File.loadable
    def mesh(self):
        import meshio

        return meshio.read(self.file_info.path)
