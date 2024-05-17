import os
from typing import Optional, Type

from ..utils import get_mimes, get_path_relative_to_root
from ..utils import solidipes_logging as logging
from .cached_metadata import CachedMetadata
from .data_container import DataContainer
from .mime_types import get_extension, get_mime_type, get_possible_extensions, is_valid_extension

logger = logging.getLogger()


class File(CachedMetadata, DataContainer):
    """Abstract container class for file metadata

    A File can be read from disk and may contain multiple DataContainer
    entries.
    """

    #: List of supported mime types. Override in subclasses.
    supported_mime_types = []
    #: List of additionally supported file extensions. Override in subclasses.
    supported_extensions = []

    def __init__(self, path=None):
        if path is None:
            raise RuntimeError("File need a path to be initialized")

        logger.debug(f"Loading a file as data container {path}")
        self.path = path
        self._discussions = []
        self._archived_discussions = False
        super().__init__(
            unique_identifier=get_path_relative_to_root(path),
            name=os.path.basename(path),
        )

    @CachedMetadata.cached_property
    def modified_time(self):
        return os.path.getmtime(self.path)

    @CachedMetadata.cached_property
    def preferred_loader_name(self):
        return self.__class__.__name__

    def add_message(self, author, msg):
        self._discussions = self.discussions
        self._discussions.append((author, msg))
        self.set_cached_metadata_entry("discussions", self._discussions)

    def archive_discussions(self, flag=True):
        self._archived_discussions = flag
        self.set_cached_metadata_entry("archived_discussions", self._archived_discussions)

    def _valid_loading(self):
        return super()._valid_loading() and self._valid_extension()

    def _valid_extension(self):
        if self.file_info.path in get_mimes():
            return True

        res = is_valid_extension(self.file_info.path, self.file_info.type)

        if not res:
            self.errors.append(
                f"Mime type '{self.file_info.type}' not matching extension '{os.path.splitext(self.file_info.path)[1]}'"
            )
        return res

    @CachedMetadata.cached_loadable
    def discussions(self):
        return self._discussions

    @CachedMetadata.cached_loadable
    def archived_discussions(self):
        return self._archived_discussions

    @CachedMetadata.cached_loadable
    def valid_loading(self):
        return self._valid_loading()

    @DataContainer.loadable
    def file_stats(self):
        stats = os.stat(self.path)
        return stats

    @CachedMetadata.cached_loadable
    def file_info(self):
        stats = self.file_stats
        mime_type, charset = get_mime_type(self.path)
        return DataContainer({
            "size": stats.st_size,
            "changed_time": stats.st_ctime,
            "created_time": stats.st_ctime,
            "modified_time": stats.st_mtime,
            "permissions": stats.st_mode,
            "owner": stats.st_uid,
            "group": stats.st_gid,
            "path": self.path,
            "type": mime_type,
            "charset": charset,
            "extension": get_extension(self.path),
        })

    @classmethod
    def check_file_support(cls, path):
        """Check mime type, then extension of file"""

        mime_type, _ = get_mime_type(path)

        for supported_mime_type in cls.supported_mime_types:
            if mime_type.startswith(supported_mime_type):
                return True

        extension = get_extension(path)

        if extension in cls.supported_extensions:
            return True

        extensions = get_possible_extensions(mime_type)
        for e in extensions:
            if e in cls.supported_extensions:
                return True

        return False


def load_file(path):
    """Load a file from path into the appropriate object type"""

    import os

    from .abaqus import Abaqus
    from .binary import Binary
    from .code_snippet import CodeSnippet
    from .geof_mesh import GeofMesh
    from .hdf5 import HDF5
    from .image import Image
    from .image_sequence import ImageSequence
    from .matlab import MatlabData
    from .notebook import Notebook
    from .pdf import PDF
    from .pyvista_mesh import PyvistaMesh
    from .symlink import SymLink
    from .table import Table
    from .text import Markdown, Text
    from .video import Video
    from .xdmf import XDMF
    from .xml import XML

    # Note: the first matching type is used
    loader_list = [
        Table,
        PyvistaMesh,
        ImageSequence,
        Image,
        Markdown,
        Text,
        CodeSnippet,
        GeofMesh,
        Video,
        PDF,
        MatlabData,
        HDF5,
        XDMF,
        XML,
        Abaqus,
        Notebook,
        Binary,  # Needs to be at the bottom always!
    ]

    if os.path.islink(path):
        return SymLink(path=path)

    if not os.path.isfile(path):
        raise FileNotFoundError(f'File "{path}" does not exist')

    # Get cached preferred loader
    loader_dict = {loader.__name__: loader for loader in loader_list}
    preferred_loader = get_cached_preferred_loader(path, loader_dict)

    if preferred_loader:
        return preferred_loader(path=path)

    # If no cached preferred loader, try to find a loader
    for loader in loader_list:
        if loader.check_file_support(path):
            return loader(path=path)

    # If no extension or unknown extension, assume binary
    return Binary(path=path)


def get_cached_preferred_loader(path: str, loader_dict: dict[str, Type[File]]) -> Optional[Type[File]]:
    """Get the preferred loader for a file from global cache"""

    from .cached_metadata import CachedMetadata

    unique_identifier = get_path_relative_to_root(path)
    preferred_loader_name = (
        CachedMetadata.get_global_cached_metadata().get(unique_identifier, {}).get("preferred_loader_name", None)
    )

    return loader_dict.get(preferred_loader_name, None)
