********************************************************************************
Gaussian Curvature
********************************************************************************

This example demonstrates how to compute the Gaussian curvature of a mesh using COMPAS libigl.

.. literalinclude:: example_curvature_gaussian.py
   :language: python

The example:

1. Loads a sample mesh (beetle)
2. Computes Gaussian curvature at each vertex
3. Visualizes the curvature values using color mapping

Key functions used:
 * :func:`compas_libigl.get_beetle` - Get sample mesh
 * :func:`compas_libigl.trimesh_gaussian_curvature` - Compute Gaussian curvature
