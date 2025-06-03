import compas
from compas_libigl.isolines import trimesh_isolines, groupsort_isolines
from compas.datastructures import Mesh
import numpy as np


def test_trimesh_isolines():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    mesh.quads_to_triangles()
    M = mesh.to_vertices_and_faces()
    scalars = np.array(mesh.vertices_attribute("z"), dtype=np.float64)
    # Calculate mean z value for isovalue
    mean_z = np.mean(scalars)
    isovalues = np.array([mean_z], dtype=np.float64)
    vertices, edges, index = trimesh_isolines(M, scalars, isovalues)
    assert len(vertices) > 0
    assert len(edges) > 0


def test_groupsort_isolines():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    mesh.quads_to_triangles()
    M = mesh.to_vertices_and_faces()
    scalars = np.array(mesh.vertices_attribute("z"), dtype=np.float64)
    # Calculate mean z value for isovalue
    mean_z = np.mean(scalars)
    isovalues = np.array([mean_z], dtype=np.float64)
    vertices, edges, index = trimesh_isolines(M, scalars, isovalues)
    polyline_groups = groupsort_isolines(vertices, edges, index)
    assert len(polyline_groups) > 0
