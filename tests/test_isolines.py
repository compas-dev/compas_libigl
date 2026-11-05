import compas
from compas.datastructures import Mesh
from compas.geometry import FaceTriangulation
from compas_libigl.isolines import trimesh_isolines
import numpy as np
import pytest


def test_trimesh_isolines():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    tessellation = mesh.triangulated(FaceTriangulation())
    scalars = np.array(mesh.vertices_attribute("z"), dtype=np.float64)
    meshdata = tessellation.to_vertices_and_triangles()
    vertices, edges = trimesh_isolines(meshdata, scalars, number_of_isolines=1)
    assert len(vertices) > 0
    assert len(edges) > 0


def test_trimesh_isolines_validates_inputs():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    tessellation = mesh.triangulated(FaceTriangulation())
    scalars = np.array(mesh.vertices_attribute("z"), dtype=np.float64)
    with pytest.raises(ValueError):
        trimesh_isolines(tessellation.to_vertices_and_triangles(), scalars[:-1], number_of_isolines=1)
    with pytest.raises(ValueError):
        trimesh_isolines(tessellation.to_vertices_and_triangles(), scalars, number_of_isolines=0)
