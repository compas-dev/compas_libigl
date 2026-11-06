import compas
from compas_libigl.meshing import (
    trimesh_remesh_along_isoline,
    trimesh_remesh_along_isolines,
    trimesh_cut_mesh,
    trimesh_face_components,
)
from compas.datastructures import Mesh
from compas.geometry import PolygonalSurface
from compas.geometry import Tessellation


def test_trimesh_remesh_along_isoline():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    triangle_mesh = mesh.triangulated()
    scalars = mesh.vertices_attribute("z")
    mean_z = sum(scalars) / len(scalars)
    vertices, triangles = trimesh_remesh_along_isoline(triangle_mesh.to_vertices_and_faces(), scalars, mean_z)
    assert len(vertices) > 0
    assert len(triangles) > 0
    assert Mesh.from_vertices_and_faces(vertices, triangles).number_of_faces() == len(triangles)
    assert len(PolygonalSurface(vertices, triangles).faces) == len(triangles)
    assert len(Tessellation(vertices, triangles).triangles) == len(triangles)


def test_trimesh_remesh_along_isolines():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    triangle_mesh = mesh.triangulated()
    M = triangle_mesh.to_vertices_and_faces()
    scalars = mesh.vertices_attribute("z")
    z_min, z_max = min(scalars), max(scalars)
    # Create 5 evenly spaced isolines
    isovalues = [z_min + i * (z_max - z_min) / 5 for i in range(1, 5)]
    V2, F2, S2, G2 = trimesh_remesh_along_isolines(M=M, scalars=scalars, isovalues=isovalues)
    assert len(V2) > 0
    assert len(F2) > 0
    assert len(S2) == len(V2)
    assert len(G2) == len(F2)


def test_trimesh_cut_mesh():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    triangle_mesh = mesh.triangulated()
    M = triangle_mesh.to_vertices_and_faces()
    V, F = M
    # Create cut flags: all ones means cut all edges
    cuts = [[1, 1, 1] for _ in F]
    Vn, Fn = trimesh_cut_mesh(M=M, cuts=cuts)
    # After cutting all edges, we should have more vertices
    assert len(Vn) >= len(V)
    assert len(Fn) == len(F)


def test_trimesh_face_components():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    triangle_mesh = mesh.triangulated()
    M = triangle_mesh.to_vertices_and_faces()
    C = trimesh_face_components(M=M)
    # Component IDs, one per face
    assert len(C) == len(M[1])
    # Connected mesh should have single component (component 0)
    assert max(C) == 0
