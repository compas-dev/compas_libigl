#pragma once

#include "compas.hpp"
#include <igl/planarize_quad_mesh.h>
#include <Eigen/Core>

/**
 * Planarize a quad mesh by iteratively projecting faces onto their best-fit planes.
 *
 * @param V The vertex matrix of the quad mesh (n x 3).
 * @param F The face matrix of the quad mesh (m x 4).
 * @param maxiter Maximum number of iterations.
 * @param threshold Convergence threshold for planarity.
 * @return Tuple of (vertices, planarity error).
 */
std::tuple<
    compas::RowMatrixXd,
    double>
quadmesh_planarize(
    compas::RowMatrixXd V,
    compas::RowMatrixXi F,
    int maxiter,
    double threshold
);