#pragma once

#include "compas.hpp"
#include <igl/grad.h>
#include <Eigen/Core>
#include <Eigen/Sparse>

/**
 * Compute the gradient operator for a triangle mesh.
 *
 * @param V The vertex positions of the mesh.
 * @param F The face indices of the mesh.
 * @return The gradient operator as a sparse matrix of size 3F x V.
 */
Eigen::SparseMatrix<double> trimesh_grad(
    Eigen::Ref<const compas::RowMatrixXd> V,
    Eigen::Ref<const compas::RowMatrixXi> F
);
