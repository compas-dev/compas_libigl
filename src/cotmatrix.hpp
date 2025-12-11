#pragma once

#include "compas.hpp"
#include <igl/cotmatrix.h>
#include <igl/cotmatrix_entries.h>
#include <Eigen/Core>
#include <Eigen/Sparse>

/**
 * Compute the cotangent Laplacian matrix of a triangle mesh.
 *
 * @param V The vertex positions of the mesh.
 * @param F The face indices of the mesh.
 * @return The cotangent Laplacian as a sparse matrix.
 */
Eigen::SparseMatrix<double> trimesh_cotmatrix(
    Eigen::Ref<const compas::RowMatrixXd> V,
    Eigen::Ref<const compas::RowMatrixXi> F
);

/**
 * Compute the cotangent values for each edge in each triangle of a mesh.
 *
 * @param V The vertex positions of the mesh.
 * @param F The face indices of the mesh.
 * @return A matrix of size F x 3 containing cotangent values per edge.
 */
compas::RowMatrixXd trimesh_cotmatrix_entries(
    Eigen::Ref<const compas::RowMatrixXd> V,
    Eigen::Ref<const compas::RowMatrixXi> F
);
