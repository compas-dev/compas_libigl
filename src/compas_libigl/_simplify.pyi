from compas.typing import Float64Array
from compas.typing import Int32Array

def ramer_douglas_peucker(
    P: Float64Array,
    threshold: float,
) -> tuple[Float64Array, Int32Array, Float64Array]: ...
