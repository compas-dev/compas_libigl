from compas.typing import Float64Array
from compas.typing import Int32Array
from compas.typing import RayMeshHit

def intersection_ray_mesh(
    point: Float64Array,
    direction: Float64Array,
    V: Float64Array,
    F: Int32Array,
) -> list[RayMeshHit]: ...
def intersection_rays_mesh(
    points: Float64Array,
    directions: Float64Array,
    V: Float64Array,
    F: Int32Array,
) -> list[list[RayMeshHit]]: ...
