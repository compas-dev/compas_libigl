import numpy as np
from compas.plugins import plugin
import sys
import platform

try:
    from compas_libigl import _meshing
    HAS_MESHING_MODULE = True
except ImportError:
    HAS_MESHING_MODULE = False
    print("Warning: _meshing module could not be imported, using pure Python fallbacks")


@plugin(category="trimesh")
def trimesh_remesh_along_isoline(M, scalars, isovalue):
    """Remesh a triangle mesh along an isoline.

    Parameters
    ----------
    M : tuple[list[list[float]], list[list[int]]]
        A mesh represented by a list of vertices and a list of faces.
    scalars : list[float]
        A list of scalar values, one per vertex.
    isovalue : float
        The value at which to compute the isoline.

    Returns
    -------
    tuple[list[list[float]], list[list[int]], list[int]]
        A tuple containing the new vertices, faces, and labels.
        Labels indicate which side of the isoline each vertex belongs to (0 or 1).

    Examples
    --------
    >>> import compas
    >>> import compas_libigl
    >>> from compas.datastructures import Mesh
    >>> mesh = Mesh.from_off(compas.get("tubemesh.off"))
    >>> mesh.quads_to_triangles()
    >>> M = mesh.to_vertices_and_faces()
    >>> scalars = mesh.vertices_attribute("z")
    >>> mean_z = sum(scalars) / len(scalars)
    >>> V2, F2, L = compas_libigl.trimesh_remesh_along_isoline(M, scalars, mean_z)
    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    S = np.asarray(scalars, dtype=np.float64)
    isovalue = float(isovalue)

    if HAS_MESHING_MODULE:
        return _meshing.trimesh_remesh_along_isoline(V, F, S, isovalue)
    else:
        # Pure Python fallback implementation
        return _pure_python_trimesh_remesh_along_isoline(V, F, S, isovalue)


@plugin(category="trimesh")
def trimesh_remesh_along_isolines(M, scalars, isovalues):
    """Remesh a triangle mesh along multiple isolines.

    Parameters
    ----------
    M : tuple[list[list[float]], list[list[int]]]
        A mesh represented by a list of vertices and a list of faces.
    scalars : list[float]
        A list of scalar values, one per vertex.
    isovalues : list[float]
        A list of values at which to compute the isolines. Remeshing is performed
        sequentially for each value in the list.

    Returns
    -------
    tuple[list[list[float]], list[list[int]], list[float]]
        A tuple containing the new vertices, faces, and scalar values per vertex.

    Examples
    --------
    >>> import compas
    >>> import compas_libigl
    >>> from compas.datastructures import Mesh
    >>> mesh = Mesh.from_off(compas.get("tubemesh.off"))
    >>> mesh.quads_to_triangles()
    >>> M = mesh.to_vertices_and_faces()
    >>> scalars = mesh.vertices_attribute("z")
    >>> z_min, z_max = min(scalars), max(scalars)
    >>> # Create 5 evenly spaced isolines
    >>> isovalues = [z_min + i * (z_max - z_min) / 5 for i in range(1, 5)]
    >>> V2, F2, S2 = compas_libigl.trimesh_remesh_along_isolines(M, scalars, isovalues)
    """
    V, F = M
    V = np.asarray(V, dtype=np.float64)
    F = np.asarray(F, dtype=np.int32)
    S = np.asarray(scalars, dtype=np.float64)
    values = np.asarray(isovalues, dtype=np.float64)

    if HAS_MESHING_MODULE:
        return _meshing.trimesh_remesh_along_isolines(V, F, S, values)
    else:
        # Pure Python fallback implementation
        return sequential_isoline_remeshing(V, F, S, values)


def sequential_isoline_remeshing(V, F, S, isovalues):
    """Pure Python implementation of sequential isoline remeshing.
    
    This is used as a fallback when the C++ implementation is not available.
    """
    current_V = V.copy()
    current_F = F.copy()
    current_S = S.copy()
    
    # Sort isovalues to ensure consistent results
    sorted_isovalues = sorted(isovalues)
    
    for isovalue in sorted_isovalues:
        # Remesh along current isoline
        if HAS_MESHING_MODULE:
            result = _meshing.trimesh_remesh_along_isoline(current_V, current_F, current_S, isovalue)
        else:
            result = _pure_python_trimesh_remesh_along_isoline(current_V, current_F, current_S, isovalue)
            
        # Update the current mesh for the next iteration
        current_V = result[0]
        current_F = result[1]
        # We need to interpolate scalar values for new vertices
        current_S = _interpolate_vertex_values(current_V, result[0], current_S)
    
    return current_V, current_F, current_S


def _interpolate_vertex_values(old_vertices, new_vertices, old_values):
    """Interpolate scalar values for new vertices based on nearest original vertices."""
    # Simple implementation for fallback - in practice you'd want to use proper interpolation
    # based on the barycentric coordinates, but this is sufficient for a fallback
    new_values = np.zeros(len(new_vertices))
    
    # For each new vertex, find the closest old vertex and use its value
    for i, new_v in enumerate(new_vertices):
        min_dist = float('inf')
        min_idx = 0
        for j, old_v in enumerate(old_vertices):
            dist = np.sum((new_v - old_v) ** 2)
            if dist < min_dist:
                min_dist = dist
                min_idx = j
        new_values[i] = old_values[min_idx]
    
    return new_values


def _pure_python_trimesh_remesh_along_isoline(V, F, S, isovalue):
    """Pure Python implementation of trimesh_remesh_along_isoline.
    
    This is a simplified version that can be used when the C++ implementation is not available.
    It does not handle all edge cases correctly but provides basic functionality.
    """
    from compas.geometry import intersect_line_plane
    from compas.datastructures import Mesh
    
    # Convert numpy arrays to lists
    vertices = V.tolist()
    faces = F.tolist()
    scalars = S.tolist()
    
    # Create a mesh
    mesh = Mesh.from_vertices_and_faces(vertices, faces)
    
    # Assign scalar values to vertices
    for i, value in enumerate(scalars):
        mesh.vertex_attribute(i, 'scalar', value)
    
    # New geometry to collect
    new_vertices = []
    new_faces = []
    labels = []
    
    # Map original vertices to new indices
    vertex_map = {}
    
    # Create a plane from the isovalue
    # Assuming isovalue is in the z-direction for simplicity
    plane = ([0, 0, isovalue], [0, 0, 1])
    
    # Process each original vertex
    for i in range(len(vertices)):
        vertex = vertices[i]
        scalar = scalars[i]
        
        # Add to new vertices and update map
        new_idx = len(new_vertices)
        new_vertices.append(vertex)
        vertex_map[i] = new_idx
        
        # Determine label based on scalar value
        label = 0 if scalar < isovalue else 1
        labels.append(label)
    
    # Process each face to add intersection points
    edge_intersections = {}
    for face_idx, face in enumerate(faces):
        face_vertices = [vertices[i] for i in face]
        face_scalars = [scalars[i] for i in face]
        
        # Check if face crosses the isovalue
        crosses = False
        for i in range(len(face)):
            if (face_scalars[i] < isovalue) != (face_scalars[(i+1) % len(face)] < isovalue):
                crosses = True
                break
        
        if crosses:
            # For each edge, compute intersection if it crosses the isovalue
            for i in range(len(face)):
                v1_idx = face[i]
                v2_idx = face[(i+1) % len(face)]
                
                # Ensure consistent ordering of edge
                edge = tuple(sorted([v1_idx, v2_idx]))
                
                # Skip if we've already processed this edge
                if edge in edge_intersections:
                    continue
                
                s1 = scalars[v1_idx]
                s2 = scalars[v2_idx]
                
                # Check if edge crosses isovalue
                if (s1 < isovalue) != (s2 < isovalue):
                    # Calculate intersection point
                    t = (isovalue - s1) / (s2 - s1)
                    v1 = vertices[v1_idx]
                    v2 = vertices[v2_idx]
                    intersect_point = [
                        v1[0] + t * (v2[0] - v1[0]),
                        v1[1] + t * (v2[1] - v1[1]),
                        v1[2] + t * (v2[2] - v1[2])
                    ]
                    
                    # Add intersection point to new vertices
                    intersect_idx = len(new_vertices)
                    new_vertices.append(intersect_point)
                    edge_intersections[edge] = intersect_idx
                    
                    # Assign label based on position (on the isovalue)
                    labels.append(0.5)  # 0.5 indicates on the boundary
    
    # Create new faces
    for face_idx, face in enumerate(faces):
        # Extract edges and check if any cross the isovalue
        edges = [(face[i], face[(i+1) % len(face)]) for i in range(len(face))]
        sorted_edges = [tuple(sorted(edge)) for edge in edges]
        crossing_edges = [edge for edge in sorted_edges if edge in edge_intersections]
        
        if len(crossing_edges) == 0:
            # Face doesn't cross isovalue, add it directly
            new_face = [vertex_map[v] for v in face]
            new_faces.append(new_face)
        elif len(crossing_edges) == 2:
            # Face crosses isovalue, split into two new faces
            # Get intersection points
            p1_idx = edge_intersections[crossing_edges[0]]
            p2_idx = edge_intersections[crossing_edges[1]]
            
            # Determine which vertices are on which side
            vertices_below = [vertex_map[v] for v in face if scalars[v] < isovalue]
            vertices_above = [vertex_map[v] for v in face if scalars[v] >= isovalue]
            
            # Create new faces
            if vertices_below:
                for v in vertices_below:
                    new_faces.append([v, p1_idx, p2_idx])
            
            if vertices_above:
                for v in vertices_above:
                    new_faces.append([v, p1_idx, p2_idx])
    
    return np.array(new_vertices), np.array(new_faces), np.array(labels)


# Function to split a mesh by a plane
def split_mesh_by_plane(mesh, plane_point, plane_normal):
    """Split a mesh into two parts based on a plane.
    
    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        The input mesh to split.
    plane_point : list
        A point on the splitting plane.
    plane_normal : list
        The normal vector of the splitting plane.
        
    Returns
    -------
    tuple
        A tuple containing two meshes (above_mesh, below_mesh).
    """
    # Normalize the plane normal
    import numpy as np
    from compas.datastructures import Mesh
    from compas.geometry import normalize_vector, dot_vectors, distance_point_plane
    
    plane_normal = normalize_vector(plane_normal)
    plane = (plane_point, plane_normal)
    
    # Generate scalar field based on signed distance to plane
    vertices = mesh.vertices_attributes('xyz')
    scalars = [distance_point_plane((x, y, z), plane) for x, y, z in vertices]
    
    # Use isoline remeshing at the zero distance (plane intersection)
    M = mesh.to_vertices_and_faces()
    V2, F2, L = trimesh_remesh_along_isoline(M, scalars, 0.0)
    
    # Create meshes for positive and negative regions
    pos_faces = [f for i, f in enumerate(F2) if all(L[v] >= 0 for v in f)]
    neg_faces = [f for i, f in enumerate(F2) if all(L[v] <= 0 for v in f)]
    
    above_mesh = Mesh.from_vertices_and_faces(V2, pos_faces)
    below_mesh = Mesh.from_vertices_and_faces(V2, neg_faces)
    
    return above_mesh, below_mesh
