import pytest

from compas_libigl.boundaries import trimesh_boundaries
from compas_libigl.cotmatrix import trimesh_cotmatrix
from compas_libigl.cotmatrix import trimesh_cotmatrix_entries
from compas_libigl.curvature import trimesh_gaussian_curvature
from compas_libigl.curvature import trimesh_principal_curvature
from compas_libigl.geodistance import trimesh_geodistance_multiple
from compas_libigl.grad import trimesh_grad
from compas_libigl.intersections import intersection_rays_mesh
from compas_libigl.mapping import map_mesh
from compas_libigl.meshing import trimesh_cut_mesh
from compas_libigl.meshing import trimesh_face_components
from compas_libigl.meshing import trimesh_remesh_along_isolines


VERTICES = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]]
QUAD_MESH = (VERTICES, [[0, 1, 2, 3]])
TRIANGLE_MESH = (VERTICES[:3], [[0, 1, 2]])


@pytest.mark.parametrize(
    "operation",
    [
        lambda: trimesh_boundaries(QUAD_MESH),
        lambda: trimesh_cotmatrix(QUAD_MESH),
        lambda: trimesh_cotmatrix_entries(QUAD_MESH),
        lambda: trimesh_gaussian_curvature(QUAD_MESH),
        lambda: trimesh_principal_curvature(QUAD_MESH),
        lambda: trimesh_geodistance_multiple(QUAD_MESH, [0]),
        lambda: trimesh_grad(QUAD_MESH),
        lambda: intersection_rays_mesh([([0.0, 0.0, 1.0], [0.0, 0.0, -1.0])], QUAD_MESH),
        lambda: trimesh_cut_mesh(QUAD_MESH, [[0, 0, 0]]),
        lambda: trimesh_face_components(QUAD_MESH),
        lambda: trimesh_remesh_along_isolines(QUAD_MESH, [0.0, 1.0, 1.0, 0.0], [0.5]),
        lambda: map_mesh(QUAD_MESH, TRIANGLE_MESH),
    ],
)
def test_triangle_operations_reject_nontriangle_faces(operation):
    with pytest.raises(ValueError, match=r"shape \(M, 3\)"):
        operation()
