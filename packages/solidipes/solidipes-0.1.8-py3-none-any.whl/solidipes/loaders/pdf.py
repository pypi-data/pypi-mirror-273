import base64

from .. import viewers
from .file import File


class PDF(File):
    """Image loaded as base64"""

    supported_mime_types = ["application/pdf"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.default_viewer = viewers.PDF

    @File.loadable
    def pdf(self):
        with open(self.file_info.path, "rb") as f:
            try:
                base64_pdf = base64.b64encode(f.read()).decode("utf-8")
                return base64_pdf
            except Exception:
                raise RuntimeError(f"could not load file {self.file_info.path}")
