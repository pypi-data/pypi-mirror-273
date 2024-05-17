from .. import viewers
from .file import File


class Text(File):
    """Text file, potentially formatted with markdown"""

    supported_mime_types = ["text/plain"]
    supported_extensions = ["txt"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.default_viewer = viewers.Text

    @File.loadable
    def text(self):
        text = ""
        with open(self.file_info.path, "r") as f:
            text = f.read()
        return text


class Markdown(Text):
    """Markdown file"""

    supported_mime_types = ["text/markdown"]
    supported_extensions = ["md"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.default_viewer = viewers.MarkdownViewer
