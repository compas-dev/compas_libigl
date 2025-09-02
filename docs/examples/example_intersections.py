import compas
import numpy as np
from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Line
from compas.geometry import Point
from compas_viewer import Viewer

from compas_libigl.intersections import intersection_rays_mesh
from compas_libigl.intersections import barycenter_to_point

# ==============================================================================
# Input geometry
# ==============================================================================

mesh = Mesh.from_obj(compas.get("tubemesh.obj"))

trimesh = mesh.copy()
trimesh.quads_to_triangles()

# ==============================================================================
# Rays
# ==============================================================================

base = Point(*mesh.centroid())
base.z = 0

theta = np.linspace(0, np.pi, 20, endpoint=False)
phi = np.linspace(0, 2 * np.pi, 20, endpoint=False)
theta, phi = np.meshgrid(theta, phi)
theta = theta.ravel()
phi = phi.ravel()
r = 1.0
x = r * np.sin(theta) * np.cos(phi) + base.x
y = r * np.sin(theta) * np.sin(phi) + base.y
z = r * np.cos(theta)

xyz = np.vstack((x, y, z)).T
mask = xyz[:, 2] > 0
hemi = xyz[mask]

rays = []
for x, y, z in hemi:
    point = Point(x, y, z)
    vector = point - base
    vector.unitize()
    rays.append((base, vector))

# ==============================================================================
# Intersections
# ==============================================================================

index_face = {index: face for index, face in enumerate(mesh.faces())}

hits_per_ray = intersection_rays_mesh(rays, mesh.to_vertices_and_faces())

intersections = []
for ray, hits in zip(rays, hits_per_ray):
    if hits:
        idx, u, v, w = hits[0]
        vertices = mesh.face_vertices(idx)
        p1 = mesh.vertex_coordinates(vertices[0])
        p2 = mesh.vertex_coordinates(vertices[1])
        p3 = mesh.vertex_coordinates(vertices[2])
        point = barycenter_to_point(u, v, w, p1, p2, p3)
        intersections.append(point)

# ==============================================================================
# Visualisation
# ==============================================================================

viewer = Viewer(width=1600, height=900)

viewer.scene.add(mesh, opacity=0.7, show_points=False)

for intersection in intersections:
    viewer.scene.add(Line(base, intersection), linecolor=Color.blue(), linewidth=3)

viewer.show()
