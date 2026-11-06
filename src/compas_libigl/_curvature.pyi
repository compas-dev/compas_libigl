from compas.typing import Float64Array
from compas.typing import Int32Array

def trimesh_principal_curvature(
    V: Float64Array,
    F: Int32Array,
    radius: int = 5,
) -> tuple[Float64Array, Float64Array, Float64Array, Float64Array]: ...
def trimesh_gaussian_curvature(V: Float64Array, F: Int32Array) -> Float64Array: ...
