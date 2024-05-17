from pyvista.utilities.fileio import from_meshio

from .parse_inp import read_geof
from .pyvista_mesh import PyvistaMesh


class GeofMesh(PyvistaMesh):
    """Mesh file loaded with pyvista"""

    supported_extensions = ["geof"]

    @PyvistaMesh.loadable
    def mesh(self):
        return from_meshio(read_geof(self.file_info.path))
