import math
import numpy as np
import compas_libigl as igl
from compas.colors import Color, ColorMap
from compas.geometry import Plane
from compas.datastructures import Mesh
from compas.geometry import Rotation
from compas.geometry import Scale
from compas_viewer import Viewer


# Load and transform mesh
mesh = Mesh.from_off(igl.get_beetle())
Rx = Rotation.from_axis_and_angle([1, 0, 0], math.radians(90))
Rz = Rotation.from_axis_and_angle([0, 0, 1], math.radians(90))
S = Scale.from_factors([10, 10, 10])
mesh.transform(S * Rz * Rx)

# Set scalar values (using z-coordinate for this example)
for vertex in mesh.vertices():
    mesh.vertex_attribute(vertex, "scalar", mesh.vertex_attribute(vertex, "z"))

# Get scalar range
scalar_values = mesh.vertices_attribute("scalar")
min_value, max_value = min(scalar_values), max(scalar_values)

# Define 5 isovalues evenly spaced between min and max
isovalues = [min_value + i * (max_value - min_value) / 5 for i in range(1, 5)]
print(f"Remeshing along {len(isovalues)} isolines: {isovalues}")


vertices_and_faces = mesh.to_vertices_and_faces()
V2, F2, S2 = igl.trimesh_remesh_along_isolines(
    vertices_and_faces,
    scalar_values, 
    isovalues
)

cpp_mesh = Mesh.from_vertices_and_faces(V2, F2)

viewer = Viewer()

viewer.scene.add(cpp_mesh, facecolor=Color.green(), show_lines=True, name="C++ Remeshed")
viewer.show()
