import math
import compas_libigl as igl
from compas.colors import Color, ColorMap
from compas.geometry import Plane
from compas.datastructures import Mesh
from compas.geometry import Rotation
from compas.geometry import Scale
from compas_viewer import Viewer


def compute_plane_distance(point, plane):
    """Compute signed distance from a point to a plane."""
    vector = plane.point - point
    return plane.normal.dot(vector)


def slice_mesh_with_planes(mesh, planes, attribute_name="cut", combine="min"):
    """Slice a mesh using the combined distance field from multiple planes."""
    if not planes:
        return None, None
    
    # Compute signed distances for all planes
    all_distances = []
    for plane in planes:
        distances = []
        for vertex in mesh.vertices():
            point = mesh.vertex_attributes(vertex, "xyz")
            dist = compute_plane_distance(point, plane)
            distances.append(dist)
        all_distances.append(distances)
    
    # Combine distances based on the chosen method
    if len(all_distances) == 1:
        combined_distances = all_distances[0]
    else:
        combined_distances = all_distances[0]  # Start with first plane's distances
        for distances in all_distances[1:]:  # Combine with remaining planes
            if combine == "min":
                combined_distances = [min(d1, d2) for d1, d2 in zip(combined_distances, distances)]
            elif combine == "max":
                combined_distances = [max(d1, d2) for d1, d2 in zip(combined_distances, distances)]
            elif combine == "average":
                combined_distances = [(d1 + d2) / 2 for d1, d2 in zip(combined_distances, distances)]
            elif combine == "multiply":
                combined_distances = [d1 * d2 for d1, d2 in zip(combined_distances, distances)]
    
    for vertex, distance in zip(mesh.vertices(), combined_distances):
        mesh.vertex_attribute(vertex, attribute_name, distance)

    # Remesh along the zero isoline (intersection)
    V2, F2, L = igl.trimesh_remesh_along_isoline(
        mesh.to_vertices_and_faces(),
        mesh.vertices_attribute(attribute_name),
        0
    )
    
    # Split faces based on labels
    below_faces = [f for i, f in enumerate(F2) if L[i] == 0]
    above_faces = [f for i, f in enumerate(F2) if L[i] == 1]
    
    # Get unique vertices for each part
    below_vertices = set()
    above_vertices = set()
    for face in below_faces:
        below_vertices.update(face)
    for face in above_faces:
        above_vertices.update(face)
    
    # Create vertex maps for new indices
    below_vmap = {old: new for new, old in enumerate(sorted(below_vertices))}
    above_vmap = {old: new for new, old in enumerate(sorted(above_vertices))}
    
    # Create new vertex lists
    below_verts = [V2[i] for i in sorted(below_vertices)]
    above_verts = [V2[i] for i in sorted(above_vertices)]
    
    # Remap face indices
    below_faces = [[below_vmap[v] for v in face] for face in below_faces]
    above_faces = [[above_vmap[v] for v in face] for face in above_faces]
    
    # Create new meshes
    below_mesh = Mesh.from_vertices_and_faces(below_verts, below_faces) if below_faces else None
    above_mesh = Mesh.from_vertices_and_faces(above_verts, above_faces) if above_faces else None
    
    return below_mesh, above_mesh


def recursive_slice(mesh, plane_groups, depth=0, region_id=0):
    """Recursively slice mesh with groups of planes and assign region IDs."""
    if depth >= len(plane_groups):
        return [(mesh, region_id)]
    
    below_mesh, above_mesh = slice_mesh_with_planes(mesh, plane_groups[depth], combine="min")
    
    results = []
    # Process below mesh (region_id stays the same)
    if below_mesh and below_mesh.number_of_faces() > 0:
        results.extend(recursive_slice(below_mesh, plane_groups, depth + 1, region_id))
    
    # Process above mesh (region_id gets modified)
    if above_mesh and above_mesh.number_of_faces() > 0:
        results.extend(recursive_slice(above_mesh, plane_groups, depth + 1, region_id + 2**depth))
    
    return results


# Load and transform mesh
mesh = Mesh.from_off(igl.get_beetle())
Rx = Rotation.from_axis_and_angle([1, 0, 0], math.radians(90))
Rz = Rotation.from_axis_and_angle([0, 0, 1], math.radians(90))
S = Scale.from_factors([10, 10, 10])
mesh.transform(S * Rz * Rx)

# Define different directions for planes
directions = [
    [0, 1, 1],   # Direction 1
    # [1, 0, 1],   # Direction 2
    # # Add more directions if needed
    # [1, 1, 0],   # Direction 3
]

# Create groups of planes at each offset
plane_groups = []
for i in range(-2, 3):  # Creates 5 offset positions
    # At each offset, create a group with planes in different directions
    planes_at_offset = [Plane([0, 0, i], direction) for direction in directions]
    plane_groups.append(planes_at_offset)

# Perform recursive slicing
mesh_regions = recursive_slice(mesh, plane_groups)
print(f"Number of regions: {len(mesh_regions)}")

# Setup visualization
viewer = Viewer()

# Create color gradient
cmap = ColorMap.from_mpl("viridis")

# Add each region with its color
for mesh_part, region_id in mesh_regions:
    if mesh_part and mesh_part.number_of_faces() > 0:
        # Normalize region_id to [0,1] for coloring
        color = cmap(region_id / (2**len(plane_groups)))
        viewer.scene.add(mesh_part, facecolor=color, show_lines=False)

viewer.show()
