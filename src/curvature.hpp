#pragma once

#include "compas.hpp"
#include <Eigen/Core>
#include <igl/gaussian_curvature.h>
#include <igl/principal_curvature.h>

/**
 * Compute the discrete gaussian curvature of a triangle mesh.
 *
 * @param V The vertex matrix of the triangle mesh (n x 3).
 * @param F The face matrix of the triangle mesh (m x 3).
 * @return A vector of gaussian curvature values per vertex.
 */
compas::VectorXd trimesh_gaussian_curvature(
    Eigen::Ref<const compas::RowMatrixXd> V,
    Eigen::Ref<const compas::RowMatrixXi> F
);

/**
 * Compute the principal curvatures and directions of a triangle mesh.
 *
 * @param V The vertex matrix of the triangle mesh (n x 3).
 * @param F The face matrix of the triangle mesh (m x 3).
 * @param radius The radius of the neighborhood for curvature computation.
 * @return A tuple of (PD1, PD2, PV1, PV2) where:
 *         - PD1: principal direction 1 per vertex (n x 3)
 *         - PD2: principal direction 2 per vertex (n x 3)
 *         - PV1: principal curvature 1 per vertex (n x 1)
 *         - PV2: principal curvature 2 per vertex (n x 1)
 */
compas::PrincipalCurvatureResult
trimesh_principal_curvature(
    Eigen::Ref<const compas::RowMatrixXd> V,
    Eigen::Ref<const compas::RowMatrixXi> F,
    int radius = 5
);