#pragma once

#include "compas.hpp"
#include <igl/massmatrix.h>
#include <Eigen/Core>
#include <Eigen/Sparse>

/**
 * Compute the mass matrix of a triangle mesh.
 *
 * @param V The vertex positions of the mesh.
 * @param F The face indices of the mesh.
 * @param type The type of mass matrix to compute ('barycentric' or 'voronoi').
 * @return The mass matrix as a sparse matrix.
 */
Eigen::SparseMatrix<double> trimesh_massmatrix(
    Eigen::Ref<const compas::RowMatrixXd> V,
    Eigen::Ref<const compas::RowMatrixXi> F,
    const std::string& type = "voronoi"
);
