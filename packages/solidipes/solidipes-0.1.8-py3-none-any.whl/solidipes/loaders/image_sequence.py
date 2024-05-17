from PIL import Image as PILImage

from .. import viewers
from .file import File
from .sequence import Sequence


class ImageSequence(Sequence, File):
    """Sequence of images loaded with PIL"""

    supported_mime_types = ["image/"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.default_viewer = viewers.Image

    @File.loadable
    def image_sequence(self):
        return PILImage.open(self.file_info.path)

    @File.loadable
    def n_frames(self):
        return self.image_sequence.n_frames

    @property
    def _element_count(self):
        return self.n_frames

    def _load_element(self, n):
        """Load a single frame"""

        self.image_sequence.seek(n)
        return self.image_sequence.copy()

    def select_frame(self, frame):
        self.select_element(frame)

    @property
    def image(self):
        # cannot be defined as loadable because it changes
        return self._current_element

    @classmethod
    def check_file_support(cls, path):
        """In addition to File class checks, also check if the file is a sequence of images"""

        if not super().check_file_support(path):
            return False

        try:
            with PILImage.open(path) as im:
                return im.is_animated  # tests whether the file contains multiple frames

        except Exception:
            return False
