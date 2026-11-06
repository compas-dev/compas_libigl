from compas.typing import Float64Array
from compas.typing import Int32Array

def planarize_quads(
    V: Float64Array,
    F: Int32Array,
    maxiter: int,
    threshold: float,
) -> Float64Array: ...
