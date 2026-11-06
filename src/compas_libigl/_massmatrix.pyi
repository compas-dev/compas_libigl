from compas.typing import Float64Array
from compas.typing import Int32Array
from scipy.sparse import csc_matrix

def trimesh_massmatrix(
    V: Float64Array,
    F: Int32Array,
    type: str = "barycentric",
) -> csc_matrix: ...
