from compas.typing import Float64Array
from compas.typing import Int32Array

def trimesh_geodistance(
    V: Float64Array,
    F: Int32Array,
    source: int,
    method: str = "heat",
) -> Float64Array: ...
def trimesh_geodistance_multiple(
    V: Float64Array,
    F: Int32Array,
    sources: Int32Array,
    method: str = "heat",
) -> Float64Array: ...
def trimesh_geodistance_exact(V: Float64Array, F: Int32Array, vid: int) -> Float64Array: ...
def trimesh_geodistance_heat(V: Float64Array, F: Int32Array, vid: int) -> Float64Array: ...
