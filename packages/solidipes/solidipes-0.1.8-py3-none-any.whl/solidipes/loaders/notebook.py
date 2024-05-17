import nbformat

from .. import viewers
from .file import File


class Notebook(File):
    """Notebook file, in Jupyter style"""

    supported_extensions = ["ipynb"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.default_viewer = viewers.Notebook

    @File.loadable
    def notebook(self):
        return nbformat.read(self.file_info.path, as_version=4)
