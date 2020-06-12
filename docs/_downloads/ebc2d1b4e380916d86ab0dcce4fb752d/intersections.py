import math
import numpy as np
import compas_libigl as igl

from compas.geometry import add_vectors, scale_vector
from compas.geometry import Point, Vector, Line, Plane, Sphere
from compas.geometry import Reflection, Translation
from compas.datastructures import Mesh

from compas_viewers.objectviewer import ObjectViewer

# ==============================================================================
# Input geometry
# ==============================================================================

mesh = Mesh.from_off(igl.get('tubemesh.off'))
mesh.quads_to_triangles()

z = mesh.vertices_attribute('z')
zmin = min(z)

T = Translation.from_vector([0, 0, -zmin])
mesh.transform(T)

# ==============================================================================
# Rays
# ==============================================================================

base = Point(-7, 0, 0)

sphere = Sphere(base, 1.0)

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
# Intersections & Reflections
# ==============================================================================

intersections = []
# reflections = []

ground = Plane([0, 0, 0], [0, 0, 1])

faces = list(mesh.faces())

for ray in rays:
    base, vector = ray
    hits = igl.intersection_ray_mesh(ray, mesh)
    if hits:
        i = hits[0][0]
        d = hits[0][3]
        if i in faces:
            n = scale_vector(mesh.face_normal(i), -1)
            x = add_vectors(base, scale_vector(vector, d))
            p = Point(*x)
            # r = base.transformed(Reflection.from_plane((p, n)))
            intersections.append(p)
            # reflections.append(r)

# ==============================================================================
# Visualisation
# ==============================================================================

viewer = ObjectViewer()

viewer.add(mesh, settings={'color': '#cccccc', 'opacity': 0.7, 'vertices.on': False})

for p in intersections:
    viewer.add(Line(base, p), settings={'edges.color': '#ff0000', 'edges.width': 2})
    # viewer.add(Line(p, r), settings={'edges.color': '#0000ff', 'edges.width': 2})

viewer.update()
viewer.show()
