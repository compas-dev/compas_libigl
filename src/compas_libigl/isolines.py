import numpy as np
from compas.geometry import Polyline
from compas.plugins import plugin

from compas_libigl import _isolines


@plugin(category="trimesh")
def trimesh_isolines(M, scalars, isovalues):
    """
    Compute isolines on a triangle mesh.

    Parameters
    ----------
    M : tuple[list[list[float]], list[list[int]]]
        A mesh represented by a tuple of (vertices, faces)
        where vertices are 3D points and faces are triangles
    scalars : list[float]
        A list of scalar values, one per vertex of the mesh.
    isovalues : list[float]
        The values at which to compute the isolines.
        Each value should be within the range of the scalar field.

    Returns
    -------
    tuple[list[list[float]], list[list[int]], list[int]]
        A tuple containing:

        * The coordinates of the isoline vertices
        * The edges between these vertices forming the isolines
        * An index per edge indicating to which isoline it belongs

    Notes
    -----
    The input mesh should be triangulated for accurate results.
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
    """
    Group and sort isoline edges into continuous polylines.

    Parameters
    ----------
    vertices : list[list[float]]
        The coordinates of the isoline vertices.
    edges : list[list[int]]
        The edges between vertices forming the isolines.
    indices : list[int]
        An index per edge indicating to which isoline it belongs.

    Returns
    -------
    list[list[compas.geometry.Polyline]]
        A list of polyline groups, where each group corresponds to an isoline level.
        Each polyline represents a continuous segment of an isoline.

    Notes
    -----
    The function attempts to create the minimum number of polylines by connecting
    edges that share vertices and have the same isovalue.
    """
    # Group edges by their index value
    edge_groups = {}
    for i, edge in enumerate(edges):
        idx = indices[i].item()  # Convert numpy array element to scalar using item()
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
