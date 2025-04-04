import compas
import compas_libigl
from compas.datastructures import Mesh


def test_quadmesh_planarize():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    M = mesh.to_vertices_and_faces()
    new_vertices = compas_libigl.quadmesh_planarize(M, kmax=10, maxdev=0.01)
    assert len(new_vertices) == mesh.number_of_vertices()
