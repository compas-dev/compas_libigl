import numpy as np
from compas.geometry import Tessellation


def as_libigl_tessellation(mesh: Tessellation):
    """Convert a tessellation to libigl's native dense-array boundary."""
    if not isinstance(mesh, Tessellation):
        raise TypeError("mesh should be a Tessellation.")

    vertices, triangles = mesh.to_vertices_and_triangles()
    V = np.asarray(vertices, dtype=np.float64, order="C").reshape((-1, 3))

    indices = np.asarray(triangles)
    if indices.size:
        limits = np.iinfo(np.int32)
        if np.any(indices < 0) or np.any(indices > limits.max):
            raise OverflowError("Tessellation indices exceed libigl's int32 range.")
    F = np.asarray(indices, dtype=np.int32, order="C").reshape((-1, 3))
    return V, F


def as_scalarfield(values, vertex_count: int):
    """Convert and validate a per-vertex scalar field."""
    scalars = np.asarray(values, dtype=np.float64)
    if scalars.ndim != 1:
        raise ValueError("scalarfield should be one-dimensional.")
    if len(scalars) != vertex_count:
        raise ValueError("scalarfield should contain one value per tessellation vertex.")
    if not len(scalars):
        raise ValueError("scalarfield should not be empty.")
    if not np.all(np.isfinite(scalars)):
        raise ValueError("scalarfield should contain only finite values.")
    return np.asarray(scalars, dtype=np.float64, order="C")


def validate_parametrisation_topology(triangles, vertex_count: int):
    """Validate topology required by libigl's boundary-based parametrisations."""
    if vertex_count == 0 or len(triangles) == 0:
        raise ValueError("Parametrisation requires a nonempty tessellation.")

    edge_uses = {}
    face_adjacency = [set() for _ in triangles]
    for face_index, triangle in enumerate(triangles):
        for u, v in ((triangle[0], triangle[1]), (triangle[1], triangle[2]), (triangle[2], triangle[0])):
            key = (min(int(u), int(v)), max(int(u), int(v)))
            uses = edge_uses.setdefault(key, [])
            uses.append((face_index, int(u), int(v)))
            if len(uses) > 2:
                raise ValueError("Parametrisation requires a manifold tessellation.")

    boundary_edges = []
    for key, uses in edge_uses.items():
        if len(uses) == 1:
            boundary_edges.append(key)
            continue
        first, second = uses
        if first[1:] != (second[2], second[1]):
            raise ValueError("Parametrisation requires consistently oriented triangles.")
        face_adjacency[first[0]].add(second[0])
        face_adjacency[second[0]].add(first[0])

    if not boundary_edges:
        raise ValueError("Parametrisation requires an open tessellation with a boundary.")

    visited = {0}
    pending = [0]
    while pending:
        pending.extend(face_adjacency[pending.pop()] - visited)
        visited.update(pending)
    if len(visited) != len(triangles):
        raise ValueError("Parametrisation requires a single connected component.")

    boundary_adjacency = {}
    for u, v in boundary_edges:
        boundary_adjacency.setdefault(u, set()).add(v)
        boundary_adjacency.setdefault(v, set()).add(u)
    if any(len(neighbors) != 2 for neighbors in boundary_adjacency.values()):
        raise ValueError("Parametrisation requires a closed manifold boundary loop.")
    boundary_visited = {next(iter(boundary_adjacency))}
    boundary_pending = list(boundary_visited)
    while boundary_pending:
        boundary_pending.extend(boundary_adjacency[boundary_pending.pop()] - boundary_visited)
        boundary_visited.update(boundary_pending)
    if len(boundary_visited) != len(boundary_adjacency):
        raise ValueError("Parametrisation requires a single boundary loop.")
