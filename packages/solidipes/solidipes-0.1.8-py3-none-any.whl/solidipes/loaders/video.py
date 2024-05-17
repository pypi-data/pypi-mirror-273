from .. import viewers
from .file import File


class Video(File):
    """Video file"""

    supported_mime_types = ["video/"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.default_viewer = viewers.Video

    @File.loadable
    def video(self):
        return open(self.file_info.path, "rb")
