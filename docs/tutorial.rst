********************************************************************************
Tutorial
********************************************************************************


Input/Output
============

High-level operations shared with COMPAS accept a
``compas.geometry.Tessellation``. The package converts its buffers to libigl's
native arrays internally. Package-specific direct bindings may retain their
native-oriented inputs and results.

.. code-block:: python

    import compas
    from compas.datastructures import Mesh
    from compas.geometry import EarClipping
    from compas.geometry import FaceTriangulation
    from compas_libigl.curvature import trimesh_gaussian_curvature

    # Load a mesh
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    
    # This package-specific direct operation retains its native-oriented tuple input.
    trimesh = mesh.copy()
    trimesh.triangulate(FaceTriangulation())
    
    # Call libigl function
    result = trimesh_gaussian_curvature(trimesh.to_vertices_and_faces())

Common Data Types
=================

* Tessellations: validated triangle geometry for shared high-level operations
* Native vertices (V): internal/direct-binding nx3 arrays
* Native faces (F): internal/direct-binding mx3 triangle-index arrays
* Scalar fields: nx1 list/array of values per vertex
* Vector fields: nx3 list/array of vectors per vertex
