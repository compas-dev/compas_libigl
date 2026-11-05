# Tutorial

Shared high-level triangle-mesh operations on this branch accept a [`compas.geometry.Tessellation`](https://compas.dev/compas/latest/api/generated/compas.geometry.Tessellation.html). Package-specific direct bindings may retain native-oriented inputs and results.

```python
from compas_libigl.curvature import trimesh_gaussian_curvature

vertices = [
    [0.0, 0.0, 0.0],
    [1.0, 0.0, 0.0],
    [0.0, 1.0, 0.0],
    [0.0, 0.0, 1.0],
]
triangles = [[0, 2, 1], [0, 1, 3], [1, 2, 3], [2, 0, 3]]

# This package-specific direct operation accepts a vertices-and-faces tuple.
values = trimesh_gaussian_curvature((vertices, triangles))
assert len(values) == len(vertices)
```

Common data conventions are:

- tessellations for shared high-level triangle-mesh operations;
- `float64` arrays with shape `(n, 3)` for native vertex coordinates;
- `int32` arrays with shape `(m, 3)` for native triangle indices;
- one-dimensional values per vertex for scalar fields;
- three-dimensional values per vertex for vector fields.

Input topology and numerical preconditions depend on the operation. Consult the [API reference](api.md) for the contract of each function.
