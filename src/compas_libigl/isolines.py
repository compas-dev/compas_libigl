import numpy as np
from compas.geometry import Polyline
from compas.plugins import plugin

from compas_libigl import _isolines


@plugin(category="trimesh")
def trimesh_isolines(M, scalars, isovalues):
    """Compute isolines on a triangle mesh using a scalarfield of data points
    assigned to its vertices.

    Parameters
    ----------
    M : tuple or :class:`compas.datastructures.Mesh`
        A mesh represented by a list of vertices and a list of faces
        or by a COMPAS mesh object.
    scalars : list
        A list of scalar values per vertex.
    num_isolines : int, optional
        Number of isolines to generate.
        Default is 10.

    Returns
    -------
    tuple
        A tuple containing:
        0. The coordinates of the polyline segments representing the isolines.
        1. The segments of the polylines.

    Examples
    --------
    >>> import compas
    >>> import compas_libigl
    >>> from compas.datastructures import Mesh
    >>> mesh = Mesh.from_off(compas.get("tubemesh.off"))
    >>> mesh.quads_to_triangles()
    >>> M = mesh.to_vertices_and_faces()
    >>> scalars = mesh.vertices_attribute("z")
    >>> vertices, edges, index = compas_libigl.trimesh_isolines(M, scalars, 50)
    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    S = np.asarray(scalars, dtype=np.float64)

    # Create evenly spaced isovalues
    ISO = np.asarray(isovalues, dtype=np.float64)

    # Note: C++ function expects (V, F, isovalues, scalars)
    iso = _isolines.trimesh_isolines(V, F, S, ISO)

    return iso[0], iso[1], iso[2]  # Return vertices and edges only


def groupsort_isolines(vertices, edges, indices):
    """Group isolines edges per value level and sort edges into paths.

    Parameters
    ----------
    vertices : list
        Isoline vertices.
    edges : list
        Isoline vertex pairs.
    indices : list
        Indices into the scalars array.

    Returns
    -------
    list
        List of groups of polylines, where each group corresponds to an isoline level.
    """

    # Group edges by their index value
    edge_groups = {}
    for i, edge in enumerate(edges):
        idx = int(indices[i])  # Convert numpy array to integer
        if idx not in edge_groups:
            edge_groups[idx] = []
        edge_groups[idx].append(edge.tolist())

    # Process each group into polylines
    polyline_groups = []
    for idx, edges in edge_groups.items():
        # Convert edges to list of vertex pairs for processing
        remaining_edges = edges.copy()
        polylines = []

        while remaining_edges:
            # Start a new polyline
            current_edge = remaining_edges.pop(0)
            current_vertices = [vertices[current_edge[0]], vertices[current_edge[1]]]
            start_vertex_idx = current_edge[0]
            end_vertex_idx = current_edge[1]

            # Try to extend the polyline
            found = True
            while found:
                found = False
                for i, edge in enumerate(remaining_edges):
                    v0, v1 = edge

                    # Check if edge connects to end of current polyline
                    if v0 == end_vertex_idx:
                        current_vertices.append(vertices[v1])
                        end_vertex_idx = v1
                        remaining_edges.pop(i)
                        found = True
                        break
                    # Check if edge connects to start of current polyline
                    elif v1 == start_vertex_idx:
                        current_vertices.insert(0, vertices[v0])
                        start_vertex_idx = v0
                        remaining_edges.pop(i)
                        found = True
                        break
                    # Check if edge needs to be reversed to connect to end
                    elif v1 == end_vertex_idx:
                        current_vertices.append(vertices[v0])
                        end_vertex_idx = v0
                        remaining_edges.pop(i)
                        found = True
                        break
                    # Check if edge needs to be reversed to connect to start
                    elif v0 == start_vertex_idx:
                        current_vertices.insert(0, vertices[v1])
                        start_vertex_idx = v1
                        remaining_edges.pop(i)
                        found = True
                        break

            # Add the completed polyline
            polylines.append(Polyline(current_vertices))

        polyline_groups.append(polylines)

    return polyline_groups
