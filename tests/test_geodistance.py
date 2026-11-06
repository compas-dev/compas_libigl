import compas
from compas.datastructures import Mesh
from compas_libigl.geodistance import trimesh_geodistance
from compas_libigl.geodistance import trimesh_geodistance_multiple


def test_trimesh_geodistance():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    triangle_mesh = mesh.triangulated()
    source = 0
    meshdata = triangle_mesh.to_vertices_and_faces()
    distances = trimesh_geodistance(meshdata, source, method="exact")
    assert len(distances) == mesh.number_of_vertices()
    distances = trimesh_geodistance(meshdata, source, method="heat")
    assert len(distances) == mesh.number_of_vertices()


def test_trimesh_geodistance_multiple():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    triangle_mesh = mesh.triangulated()
    M = triangle_mesh.to_vertices_and_faces()
    sources = [0, 1]
    distances = trimesh_geodistance_multiple(M=M, sources=sources, method="exact")
    assert len(distances) == mesh.number_of_vertices()
    distances = trimesh_geodistance_multiple(M=M, sources=sources, method="heat")
    assert len(distances) == mesh.number_of_vertices()
