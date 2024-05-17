import streamlit as st
from IPython.display import display

from .. import loaders
from ..utils import viewer_backends
from .xml import XML


class XDMF(XML):
    """Viewer for xml text files"""

    def __init__(self, data=None):
        self.xdmf = None
        super().__init__(data)
        self.compatible_data_types = [loaders.XDMF]

    def add(self, data_container):
        """Append text to the viewer"""
        super().check_data_compatibility(data_container)
        self.xdmf = data_container

    def show(self):
        content = self.xdmf.mesh
        if viewer_backends.current_backend == "jupyter notebook":
            display(content)

        elif viewer_backends.current_backend == "streamlit":
            st.write(content)
        else:  # python
            print(content)
