from compas.typing import Float64Array
from compas.typing import Int32Array

def trimesh_remesh_along_isoline(
    V1: Float64Array,
    F1: Int32Array,
    S1: Float64Array,
    s: float,
) -> tuple[Float64Array, Int32Array, Int32Array]: ...
def trimesh_remesh_along_isolines(
    V1: Float64Array,
    F1: Int32Array,
    S1: Float64Array,
    values: Float64Array,
) -> tuple[Float64Array, Int32Array, Float64Array, Int32Array]: ...
def trimesh_cut_mesh(
    V: Float64Array,
    F: Int32Array,
    cuts: Int32Array,
) -> tuple[Float64Array, Int32Array]: ...
def trimesh_face_components(F: Int32Array) -> Int32Array: ...
