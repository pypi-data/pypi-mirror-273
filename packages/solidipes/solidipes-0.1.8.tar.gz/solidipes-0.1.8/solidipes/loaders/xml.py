import xmltodict

from .. import viewers
from ..utils import solidipes_logging as logging
from .text import Text

logger = logging.getLogger()


class XML(Text):
    supported_mime_types = ["text/xml", "application/xml"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.default_viewer = viewers.XML

    @Text.loadable
    def xml(self):
        text = self.text
        xml = xmltodict.parse(text)
        return xml
