from types import SimpleNamespace

import compas
import numpy as np
import pytest
from compas.datastructures import Mesh
import compas_libigl.isolines as isolines_module
from compas_libigl.isolines import trimesh_isolines


def test_trimesh_isolines():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    triangle_mesh = mesh.triangulated()
    scalars = np.array(mesh.vertices_attribute("z"), dtype=np.float64)
    meshdata = triangle_mesh.to_vertices_and_faces()
    vertices, edges = trimesh_isolines(meshdata, scalars, number_of_isolines=1)
    assert len(vertices) > 0
    assert len(edges) > 0


def test_trimesh_isolines_validates_inputs():
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    triangle_mesh = mesh.triangulated()
    scalars = np.array(mesh.vertices_attribute("z"), dtype=np.float64)
    with pytest.raises(ValueError):
        trimesh_isolines(triangle_mesh.to_vertices_and_faces(), scalars[:-1], number_of_isolines=1)
    with pytest.raises(ValueError):
        trimesh_isolines(triangle_mesh.to_vertices_and_faces(), scalars, number_of_isolines=0)


def test_trimesh_isolines_returns_empty_result_for_constant_field(monkeypatch):
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    triangle_mesh = mesh.triangulated()
    meshdata = triangle_mesh.to_vertices_and_faces()
    scalars = np.ones(len(meshdata[0]), dtype=np.float64)
    monkeypatch.setattr(
        isolines_module,
        "_isolines",
        SimpleNamespace(trimesh_isolines=lambda *args: pytest.fail("native isolines should not be called")),
    )

    points, segments = trimesh_isolines(meshdata, scalars, number_of_isolines=2)

    assert points == []
    assert segments == []
