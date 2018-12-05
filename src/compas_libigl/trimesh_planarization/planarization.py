from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import ctypes
from ctypes import *

from compas.interop.cpp.xdarray import Array1D
from compas.interop.cpp.xdarray import Array2D


so = ctypes.cdll.LoadLibrary('planarization.so')


__all__ = ['planarize_quadmesh']


def planarize_quadmesh(vertices, faces, kmax=100, deviation=0.005):
    """Planarize a quad mesh using IGL functionality.

    Parameters
    ----------
    vertices : list
        XYZ coordinates of the mesh vertices.
    faces : list
        Vertex indices of the faces of the mesh.
    kmax : int, optional
        Maximum number of iterations.
        Default is `100`.
    deviation : float, optional
        

    """

    assert all(len(face) == 4 for face in faces), "The faces of the mesh should be quads."

    c_vertices = Array2D(vertices, 'double')
    c_faces = Array2D(faces, 'int')

    so.planarize.argtypes = [
        c_vertices.ctype,
        c_int,
        c_faces.ctype,
        c_int,
        c_int,
        c_double
    ]

    so.planarize(
        c_vertices.cdata,
        c_int(len(vertices)),
        c_faces.cdata,
        c_int(len(faces)),
        c_int(kmax),
        c_double(deviation)
    )

    return c_vertices.pydata


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas
    import compas_libigl

    from compas_libigl.plotters import MeshCompare

    from compas.datastructures import Mesh
    # from compas.plotters import MeshPlotter

    from compas.utilities import i_to_rgb
    from compas.geometry import mesh_flatness


    m1 = Mesh.from_json(compas.get('tubemesh.json'))

    v1, faces = m1.to_vertices_and_faces()

    v2 = planarize_quadmesh(v1, faces)

    m2 = Mesh.from_vertices_and_faces(v2, faces)

    d1 = mesh_flatness(m1, maxdev=0.02)
    d2 = mesh_flatness(m2, maxdev=0.02)

    plotter = MeshPlotter(m2)

    plotter.draw_faces(facecolor={fkey: i_to_rgb(d2[fkey]) for fkey in m2.faces()})

    plotter.show()
