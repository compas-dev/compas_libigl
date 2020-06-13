import math
import numpy as np
import compas_libigl as igl

from compas.geometry import add_vectors, scale_vector, cross_vectors
from compas.geometry import intersection_line_plane
from compas.geometry import Point, Vector, Line, Plane, Sphere
from compas.geometry import Reflection, Translation
from compas.datastructures import Mesh

from compas_viewers.objectviewer import ObjectViewer


def ray_mesh_intersect_reflect(ray, mesh, hit, facemap):
    base, vector = ray
    index = hit[0]
    distance = hit[3]
    face = facemap[index]
    p = base + vector * distance
    n = Vector(* mesh.face_normal(face))
    n = n.cross(vector.cross(n))
    r = base.transformed(Reflection.from_plane((p, n)))
    return p, r


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
reflections = []

ground = Plane([0, 0, 0], [0, 0, 1])

index_face = {index: face for index, face in enumerate(mesh.faces())}

for ray in rays:
    hits = igl.intersection_ray_mesh(ray, mesh)
    if hits:
        i1, r1 = ray_mesh_intersect_reflect(ray, mesh, hits[0], index_face)
        intersections.append(i1)
        vector = r1 - i1
        vector.unitize()
        ray = i1, vector
        hits = igl.intersection_ray_mesh(ray, mesh)
        if hits:
            if len(hits) > 1:
                hit = hits[1]
            else:
                hit = hits[0]
            i2, _ = ray_mesh_intersect_reflect(ray, mesh, hit, index_face)
            if (i2 - i1).length < 0.01:
                x = intersection_line_plane((i1, r1), ground)
                r1 = Point(* x)
                reflections.append((i1, r1))
            else:
                reflections.append((i1, i2))
        else:
            x = intersection_line_plane((i1, r1), ground)
            r1 = Point(* x)
            reflections.append((i1, r1))

# ==============================================================================
# Visualisation
# ==============================================================================

viewer = ObjectViewer()

viewer.add(mesh, settings={'color': '#cccccc', 'opacity': 0.5, 'edges.on': False})

for intersection in intersections:
    viewer.add(Line(base, intersection), settings={'edges.color': '#ff0000', 'edges.width': 3})

for reflection in reflections:
    viewer.add(Line(* reflection), settings={'edges.color': '#0000ff', 'edges.width': 1})

viewer.update()
viewer.show()
