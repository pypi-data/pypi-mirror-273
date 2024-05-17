import streamlit as st
from IPython.display import display

from .. import loaders
from ..utils import solidipes_logging as logging
from ..utils import viewer_backends
from .viewer import Viewer

logger = logging.getLogger()


class MatlabData(Viewer):
    """Viewer for Matlab Data .mat file"""

    def __init__(self, data=None):
        self.compatible_data_types = [loaders.MatlabData]
        #: Text to display
        self.arrays = {}
        super().__init__(data)

    def add(self, data_container):
        """Append text to the viewer"""
        self.check_data_compatibility(data_container)

        if isinstance(data_container, loaders.DataContainer):
            self.arrays.update(data_container.arrays)

    def show(self):
        for k, v in self.arrays.items():
            if viewer_backends.current_backend == "jupyter notebook":
                display(f"{k} ({type(v).__name__})")
                display(v)

            elif viewer_backends.current_backend == "streamlit":
                with st.expander(f"{k} ({type(v).__name__})"):
                    st.write(v)
            else:  # python
                print(f"{k} ({type(v).__name__})")
                print(v)
