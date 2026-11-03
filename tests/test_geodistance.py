import compas
from compas.datastructures import Mesh
from compas.geometry import FaceTriangulation
from compas_libigl.geodistance import trimesh_geodistance
from compas_libigl.geodistance import trimesh_geodistance_multiple


def test_trimesh_geodistance():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    tessellation = mesh.triangulated(FaceTriangulation())
    source = 0
    distances = trimesh_geodistance(tessellation, source, method="exact")
    assert len(distances) == mesh.number_of_vertices()
    distances = trimesh_geodistance(tessellation, source, method="heat")
    assert len(distances) == mesh.number_of_vertices()


def test_trimesh_geodistance_multiple():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    mesh.triangulate(FaceTriangulation())
    M = mesh.to_vertices_and_faces()
    sources = [0, 1]
    distances = trimesh_geodistance_multiple(M, sources, method="exact")
    assert len(distances) == mesh.number_of_vertices()
    distances = trimesh_geodistance_multiple(M, sources, method="heat")
    assert len(distances) == mesh.number_of_vertices()
