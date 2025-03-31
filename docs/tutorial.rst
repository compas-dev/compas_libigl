********************************************************************************
Tutorial
********************************************************************************

.. rst-class:: lead

:mod:`compas_libigl` provides bindings for the libigl library.
It doesn't cover the entire library, but only for specific functions.
Currently, the following functions are supported:

* :func:`compas_libigl.intersection_ray_mesh`
* :func:`compas_libigl.intersection_rays_mesh`
* :func:`compas_libigl.trimesh_boundaries`
* :func:`compas_libigl.trimesh_gaussian_curvature`
* :func:`compas_libigl.trimesh_principal_curvature`
* :func:`compas_libigl.trimesh_geodistance`
* :func:`compas_libigl.trimesh_isolines`
* :func:`compas_libigl.trimesh_massmatrix`
* :func:`compas_libigl.trimesh_harmonic`
* :func:`compas_libigl.trimesh_lscm`
* :func:`compas_libigl.trimesh_remesh_along_isoline`
* :func:`compas_libigl.quadmesh_planarize`


Input/Output
============

The function signatures of the bindings are similar to the original libigl functions.
Meshes are represented by a tuple containing a list/array of vertices and a list/array of faces.
Most functions require the input mesh to be a triangle mesh.

.. code-block:: python

    import compas
    import compas_libigl
    from compas.datastructures import Mesh

    mesh = Mesh.from_obj(compas.get("tubemesh.obj"))
    mesh.quads_to_triangles()

    V, F = mesh.to_vertices_and_faces()

    source = trimesh.vertex_sample(size=1)[0]
    distance = compas_libigl.trimesh_geodistance(
        (V, F),
        source,
        method="heat",
    )


Both Python lists and Numpy arrays are supported.

.. code-block:: python

    import numpy
    import compas
    import compas_libigl
    from compas.datastructures import Mesh

    mesh = Mesh.from_obj(compas.get("tubemesh.obj"))
    mesh.quads_to_triangles()

    vertices, faces = mesh.to_vertices_and_faces()
    V = numpy.array(vertices, dtype=float)
    F = numpy.array(faces, dtype=int)

    source = trimesh.vertex_sample(size=1)[0]
    distance = compas_libigl.trimesh_geodistance(
        (V, F),
        source,
        method="heat",
    )


Pluggables
==========


Visualisation
=============


Working in Rhino/Grasshopper
============================

The bindings are generated with PyBind11 and wrap the C++ code of libigl.
Therefore, the bindings are not compatible with IronPython and cannot be used in Rhino/Grasshopper directly.
However, they can be used in Rhino/Grasshopper through RPC.

.. code-block:: python

    import compas
    from compas.rpc import Proxy
    from compas.datastructures import Mesh
    from compas.datastructures import mesh_flatness
    from compas.colors import Color, ColorMap
    from compas.artists import Artist

    compas_libigl = Proxy('compas_libigl')

    mesh = Mesh.from_obj(compas.get("tubemesh.obj"))
    
    V, F = mesh.to_vertices_and_faces()
    V2 = compas_libigl.quadmesh_planarize((V, F), 100, 0.005)

    mesh = Mesh.from_vertices_and_faces(V2, F)
    dev = mesh_flatness(mesh, maxdev=TOL)
    cmap = ColorMap.from_two_colors(Color.white(), Color.blue())

    facecolor={
        face: (cmap(dev[face]) if dev[face] <= 1.0 else Color.red())
        for face in mesh.faces()
    }

    artist = Artist(mesh, layer="libigl::quadmesh_planarize")
    artist.draw(facecolor=facecolor, disjoint=True)
