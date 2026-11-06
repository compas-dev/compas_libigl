import compas
import numpy as np
from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Line
from compas.geometry import Point
from compas_viewer import Viewer

from compas_libigl.intersections import intersection_rays_mesh

# ==============================================================================
# Input geometry
# ==============================================================================

mesh = Mesh.from_obj(compas.get("tubemesh.obj"))
triangle_mesh = mesh.triangulated()

# ==============================================================================
# Rays
# ==============================================================================

centroid = mesh.centroid()
base = Point(centroid[0], centroid[1], centroid[2])
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

hits_per_ray = intersection_rays_mesh(rays, triangle_mesh.to_vertices_and_faces())

intersections = []
for ray, hits in zip(rays, hits_per_ray):
    if hits:
        base, vector = ray
        distance = hits[0][3]
        point = base + vector * distance
        intersections.append(point)

# ==============================================================================
# Visualisation
# ==============================================================================

viewer = Viewer(width=1600, height=900)

viewer.scene.add(mesh, opacity=0.7, show_points=False)

for intersection in intersections:
    viewer.scene.add(Line(base, intersection), linecolor=Color.blue(), linewidth=3)

viewer.show()
