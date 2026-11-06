from __future__ import annotations

from typing import TYPE_CHECKING

from compas.plugins import plugin

if TYPE_CHECKING:
    from compas.typing import RayData
    from compas.typing import RayMeshHit
    from compas.typing import VerticesFaces

__all__ = ["intersection_ray_mesh"]


@plugin(category="intersections", pluggable_name="_intersection_ray_mesh")
def intersection_ray_mesh(ray: RayData, mesh: VerticesFaces) -> list[RayMeshHit]:
    """Delegate ray-mesh intersection to the libigl implementation."""
    from compas_libigl.intersections import intersection_ray_mesh as implementation

    return implementation(ray, mesh)
