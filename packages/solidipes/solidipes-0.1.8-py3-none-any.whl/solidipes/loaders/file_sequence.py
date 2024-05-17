import os
import re

from ..utils import get_path_relative_to_root
from .cached_metadata import CachedMetadata
from .file import load_file
from .group import Group
from .sequence import Sequence


class FileSequence(Sequence, CachedMetadata, Group):
    """Sequence of files"""

    def __init__(self, pattern, paths):
        self.path = os.path.join(os.path.dirname(paths[0]), pattern)
        self._paths = paths
        self._element_count = len(paths)
        super().__init__(
            name=self.path,
            paths=paths,
            pattern=pattern,
            unique_identifier=get_path_relative_to_root(self.path),
        )
        self._set_total_size()
        del self.default_viewer  # Use files' viewers

    def _set_total_size(self):
        self.total_size = 0
        for p in self._paths:
            stats = os.stat(p)
            self.total_size += stats.st_size

    @CachedMetadata.cached_property
    def modified_time(self):
        return self.file_info.modified_time

    def _load_element(self, n):
        if n < 0 or n >= self._element_count:
            raise KeyError(f"File {n} does not exist")

        path = self._paths[n]
        return load_file(path)

    def select_file(self, n):
        self.select_element(n, update_default_viewer=True)

    @staticmethod
    def _find_groups(is_dir_path_dict: dict[str, bool]) -> dict[str, list[str]]:
        filenames = {name for name, is_dir in is_dir_path_dict.items() if not is_dir}
        groups = {}
        pattern = r"(\D+)(\d+)(\D+)"  # Matches "prefix0123suffix"

        # Find sequences
        for filename in filenames:
            match = re.match(pattern, filename)

            if match:
                prefix = match.group(1)
                suffix = match.group(3)
                wildcard = prefix + "*" + suffix

                if wildcard not in groups:
                    groups[wildcard] = []

                groups[wildcard].append(filename)

        # Remove sequences of length 1
        groups = {wildcard: filenames for wildcard, filenames in groups.items() if len(filenames) > 1}

        # Sort sequences' filenames by number (removing prefix 0s)
        for filenames in groups.values():
            filenames.sort(key=lambda name: int(re.match(pattern, name).group(2)))

        return groups
