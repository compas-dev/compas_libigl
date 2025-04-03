#pragma once

#include "compas.hpp"
#include <Eigen/Core>

/**
 * Planarize a quad mesh.
 *
 * @param V #V x 3 matrix of vertex coordinates
 * @param F #F x 4 matrix of quad indices
 * @param maxiter Maximum number of iterations
 * @param threshold Convergence threshold
 * @return Matrix of planarized vertex coordinates
 */
compas::RowMatrixXd
planarize_quads(
    compas::RowMatrixXd V,
    compas::RowMatrixXi F,
    int maxiter = 100,
    double threshold = 0.005);