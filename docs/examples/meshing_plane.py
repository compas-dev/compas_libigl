import math
import compas_libigl as igl
from compas.colors import Color
from compas.geometry import Plane
from compas.datastructures import Mesh
from compas.geometry import Rotation, Scale
from compas_viewer import Viewer


def split_mesh_by_plane(mesh, plane):
    """Split a mesh into two parts using a plane.
    
    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        The input mesh to split
    plane : compas.geometry.Plane
        The plane to split with
        
    Returns
    -------
    tuple
        Two meshes (below_mesh, above_mesh), representing parts on each side of the plane
    """
    # Calculate signed distance to the plane for all vertices
    distances = []
    for vertex in mesh.vertices():
        point = mesh.vertex_attributes(vertex, "xyz")
        vector = plane.point - point
        distance = plane.normal.dot(vector)
        distances.append(distance)
        mesh.vertex_attribute(vertex, "distance", distance)
    
    # Remesh along the zero isoline (plane intersection)
    V2, F2, L = igl.trimesh_remesh_along_isoline(
        mesh.to_vertices_and_faces(),
        distances,
        0
    )
    
    # Split faces based on labels (0 = below, 1 = above)
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
    
    # Create new meshes for each part
    below_mesh = Mesh.from_vertices_and_faces(below_verts, below_faces) if below_faces else None
    above_mesh = Mesh.from_vertices_and_faces(above_verts, above_faces) if above_faces else None
    
    return below_mesh, above_mesh


# Load and transform mesh
mesh = Mesh.from_off(igl.get_beetle())
R = Rotation.from_axis_and_angle([1, 0, 0], math.radians(90))
S = Scale.from_factors([10, 10, 10])
mesh.transform(S * R)

# Define a single cutting plane (horizontal at z=0)
cutting_plane = Plane([0, 0, 0], [0, 1, 1])

# Split the mesh
below_mesh, above_mesh = split_mesh_by_plane(mesh, cutting_plane)
print(f"Original mesh: {mesh.number_of_vertices()} vertices, {mesh.number_of_faces()} faces")
print(f"Below mesh: {below_mesh.number_of_vertices()} vertices, {below_mesh.number_of_faces()} faces")
print(f"Above mesh: {above_mesh.number_of_vertices()} vertices, {above_mesh.number_of_faces()} faces")

# Setup visualization
viewer = Viewer()

# Add both mesh parts with different colors
viewer.scene.add(below_mesh, facecolor=Color.red(), name="Below Plane")
viewer.scene.add(above_mesh, facecolor=Color.blue(), name="Above Plane")

viewer.show()
