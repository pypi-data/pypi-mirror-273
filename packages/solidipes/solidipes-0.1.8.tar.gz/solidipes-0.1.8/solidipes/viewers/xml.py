import streamlit as st
from IPython.display import display

from .. import loaders
from ..utils import viewer_backends
from .viewer import Viewer


class XML(Viewer):
    """Viewer for xml text files"""

    def __init__(self, data=None):
        # AAAAAAAAAAAAAA
        # Discussion to have with Son: this piece of code is not robust
        # It is important to distinguish construction from initialization

        self.xml = {}
        super().__init__(data)
        self.compatible_data_types = [loaders.XML]

    def add(self, data_container):
        """Append text to the viewer"""
        self.check_data_compatibility(data_container)
        self.xml.update(data_container.xml)

    def show(self):
        if viewer_backends.current_backend == "jupyter notebook":
            display(self.xml)

        elif viewer_backends.current_backend == "streamlit":
            with st.container():
                st.write(self.xml)
        else:  # python
            import yaml

            print(yaml.dump(self.xml))
