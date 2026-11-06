from compas.typing import Float64Array
from compas.typing import Int32Array
from scipy.sparse import csc_matrix

def trimesh_grad(V: Float64Array, F: Int32Array) -> csc_matrix: ...
