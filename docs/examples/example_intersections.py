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

theta = np.linspace(0, np.pi, 5, endpoint=False)
phi = np.linspace(0, 2 * np.pi, 5, endpoint=False)
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

lines = []
rays = []
for x, y, z in hemi:
    point = Point(x, y, z)
    vector = point - base
    vector.unitize()
    lines.append(Line(base, base + vector))
    rays.append((base, vector))

# ==============================================================================
# Intersections
# ==============================================================================

hits_per_rays = intersection_rays_mesh(rays, trimesh.to_vertices_and_faces())

intersection_points = []
for hits_per_ray in hits_per_rays:
    if hits_per_ray:
        for hit in hits_per_ray:
            pt, idx, u, v, w = hit
            intersection_points.append(pt)

# ==============================================================================
# Visualisation
# ==============================================================================

viewer = Viewer(width=1600, height=900)

viewer.scene.add(mesh, opacity=0.7, show_points=False)

for point in intersection_points:
    viewer.scene.add(Line(base, point), linecolor=Color.blue(), linewidth=3)
    viewer.scene.add(point, pointcolor=Color.red(), pointsize=10)

for line in lines:
    for i in range(20):
        viewer.scene.add(line.point_at(i / 20), pointcolor=Color.red(), pointsize=5)

viewer.show()
