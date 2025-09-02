import compas.geometry
import compas.datastructures
from compas_libigl.intersections import intersection_rays_mesh, intersection_ray_mesh
from compas_libigl.intersections import barycenter_to_point
from compas_viewer import Viewer
from compas.colors import Color
from compas.geometry import Line
import compas


p0 = compas.geometry.Point(2, 0, 0)
p1 = compas.geometry.Point(3 + 2, 0 - 2, 13)
p2 = compas.geometry.Point(0 - 2, 0 - 2, 10)
p3 = compas.geometry.Point(0 - 2, 2 + 2, 10)

mesh = compas.datastructures.Mesh.from_points([[p1.x, p1.y, p1.z], [p2.x, p2.y, p2.z], [p3.x, p3.y, p3.z]])

ray = (p0, compas.geometry.Vector(0, 0, 1))
hits_per_ray = intersection_ray_mesh(ray, mesh.to_vertices_and_faces())

idx, u, v, w = hits_per_ray[0][0], hits_per_ray[0][1], hits_per_ray[0][2], hits_per_ray[0][3]

index_face = {index: face for index, face in enumerate(mesh.faces())}

intersections = []
for hit in hits_per_ray:
    idx, u, v, w = hit
    point = barycenter_to_point(u, v, w, p1, p2, p3)
    intersections.append(point)

bary_coords = compas.geometry.barycentric_coordinates(intersections[0], [p1, p2, p3])
print("libigl barycentric coordinates: ", u, v, w)
print("compas barycentric coordinates: ", *bary_coords)

# ==============================================================================
# Visualisation
# ==============================================================================

viewer = Viewer(width=1600, height=900)

viewer.scene.add(mesh, opacity=0.7, show_points=False)

for intersection in intersections:
    viewer.scene.add(Line(p0, intersection), linecolor=Color.blue(), linewidth=3)

viewer.show()
