from compas.typing import Float64Array
from compas.typing import Int32Array

def trimesh_isolines(
    V: Float64Array,
    F: Int32Array,
    scalarfield: Float64Array,
    isovalues: Float64Array,
) -> tuple[Float64Array, Int32Array, Int32Array]: ...
