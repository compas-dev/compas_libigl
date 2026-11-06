from compas.typing import Float64Array
from compas.typing import Int32Array

def map_mesh_with_automatic_parameterization(
    target_v: Float64Array,
    target_f: Int32Array,
    pattern_v: Float64Array,
    pattern_f: list[list[int]],
    clip_boundaries: bool,
    simplify_borders: bool,
    fixed_vertices: list[int],
    tolerance: float,
) -> tuple[Float64Array, list[list[int]], Float64Array, list[bool], list[int]]: ...
