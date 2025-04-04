********************************************************************************
Tutorial
********************************************************************************

.. rst-class:: lead

:mod:`compas_libigl` provides bindings for the libigl library.
It doesn't cover the entire library, but provides bindings for specific geometry processing functions.
The functions are organized into the following categories:

Mesh Analysis
=============

Boundaries and Intersections
----------------------------

* :func:`compas_libigl.trimesh_boundaries` - Compute boundary loops of a mesh
* :func:`compas_libigl.intersection_ray_mesh` - Compute intersection of a ray with a mesh
* :func:`compas_libigl.intersection_rays_mesh` - Compute intersections of multiple rays with a mesh

Curvature Analysis
------------------

* :func:`compas_libigl.trimesh_gaussian_curvature` - Compute Gaussian curvature at vertices
* :func:`compas_libigl.trimesh_principal_curvature` - Compute principal curvatures and directions

Geodesic Distances
------------------

* :func:`compas_libigl.trimesh_geodistance` - Compute geodesic distance from a source vertex
* :func:`compas_libigl.trimesh_geodistance_multiple` - Compute geodesic distances from multiple source vertices

Mass Properties
---------------

* :func:`compas_libigl.trimesh_massmatrix` - Compute the mass matrix

Mesh Processing
===============

Remeshing and Isolines
----------------------

* :func:`compas_libigl.trimesh_isolines` - Extract isolines from a scalar field
* :func:`compas_libigl.groupsort_isolines` - Sort and group isolines
* :func:`compas_libigl.trimesh_remesh_along_isoline` - Remesh along a single isoline
* :func:`compas_libigl.trimesh_remesh_along_isolines` - Remesh along multiple isolines

Parameterization
----------------

* :func:`compas_libigl.trimesh_harmonic` - Compute harmonic parameterization
* :func:`compas_libigl.trimesh_lscm` - Compute least squares conformal mapping

Mesh Optimization
-----------------

* :func:`compas_libigl.quadmesh_planarize` - Planarize quad mesh faces

Utilities
=========

* :func:`compas_libigl.get` - Get sample geometry files
* :func:`compas_libigl.get_beetle` - Get the beetle mesh
* :func:`compas_libigl.get_armadillo` - Get the armadillo mesh

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
