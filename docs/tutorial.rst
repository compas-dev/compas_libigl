********************************************************************************
Tutorial
********************************************************************************


Input/Output
============

The function signatures of the bindings are similar to the original libigl functions.
Meshes are represented by a tuple containing a list/array of vertices and a list/array of faces.
Most functions require the input mesh to be a triangle mesh.

.. code-block:: python

    import compas_libigl as igl
    from compas.datastructures import Mesh

    # Load a mesh
    mesh = Mesh.from_off(igl.get_beetle())
    
    # Convert to format expected by libigl functions
    V, F = mesh.to_vertices_and_faces()
    
    # Call libigl function
    result = igl.trimesh_gaussian_curvature(V, F)

Common Data Types
=================

* Vertices (V): nx3 list/array of vertex coordinates
* Faces (F): mx3 list/array of vertex indices for triangle meshes
* Scalar fields: nx1 list/array of values per vertex
* Vector fields: nx3 list/array of vectors per vertex
