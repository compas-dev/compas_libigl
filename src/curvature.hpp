#pragma once

#include "compas.hpp"
#include <igl/gaussian_curvature.h>
#include <igl/principal_curvature.h>

namespace compas_libigl {

/**
 * Compute the discrete gaussian curvature of a triangle mesh.
 *
 * @param V The vertex matrix of the triangle mesh (n x 3).
 * @param F The face matrix of the triangle mesh (m x 3).
 * @return A vector of gaussian curvature values per vertex.
 */
Eigen::VectorXd trimesh_gaussian_curvature(
    compas::RowMatrixXd V,
    compas::RowMatrixXi F
);

/**
 * Compute the principal curvatures and directions of a triangle mesh.
 *
 * @param V The vertex matrix of the triangle mesh (n x 3).
 * @param F The face matrix of the triangle mesh (m x 3).
 * @param[out] PD1 Principal direction 1 per vertex (normalized vectors).
 * @param[out] PD2 Principal direction 2 per vertex (normalized vectors).
 * @param[out] PV1 Principal curvature value 1 per vertex (maximum curvature).
 * @param[out] PV2 Principal curvature value 2 per vertex (minimum curvature).
 */
void trimesh_principal_curvature(
    compas::RowMatrixXd V,
    compas::RowMatrixXi F,
    Eigen::MatrixXd& PD1,
    Eigen::MatrixXd& PD2,
    Eigen::VectorXd& PV1,
    Eigen::VectorXd& PV2
);

} // namespace compas_libigl