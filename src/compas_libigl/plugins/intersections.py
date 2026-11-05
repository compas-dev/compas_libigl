from __future__ import annotations

from typing import TYPE_CHECKING

from compas.plugins import plugin

if TYPE_CHECKING:
    from compas._typing import RayMeshHit
    from compas._typing import RayType
    from compas._typing import TriangleMeshInput


@plugin(category="intersections", pluggable_name="_intersection_ray_mesh")
def intersection_ray_mesh(ray: RayType, mesh: TriangleMeshInput) -> list[RayMeshHit]:
    from compas_libigl.intersections import intersection_ray_mesh as implementation

    return implementation(ray, mesh)
