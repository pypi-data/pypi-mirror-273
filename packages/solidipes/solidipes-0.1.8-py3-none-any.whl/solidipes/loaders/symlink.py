import os

from .. import viewers
from .file import File, load_file


class SymLink(File):
    """Symbolic link (special file)"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.default_viewer = viewers.SymLink  # TODO: to binary or file info

    # TODO: as sequence, if path does not exist, treat as separate file with some infos
    @File.loadable
    def linked_file(self):
        from pathlib import Path

        _path = str(Path(self.file_info.path).resolve())
        if os.path.exists(_path):
            return load_file(_path)

        return _path
