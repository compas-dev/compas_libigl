#pragma once

#include "compas.hpp"
#include <Eigen/Core>

/**
 * Compute the harmonic parametrization of a triangle mesh.
 *
 * @param V #V x 3 matrix of vertex coordinates
 * @param F #F x 3 matrix of triangle indices
 * @return UV coordinates for each vertex
 */
Eigen::MatrixXd
harmonic(
    Eigen::Ref<const compas::RowMatrixXd> V,
    Eigen::Ref<const compas::RowMatrixXi> F);

/**
 * Compute the least-squares conformal map of a triangle mesh.
 *
 * @param V #V x 3 matrix of vertex coordinates
 * @param F #F x 3 matrix of triangle indices
 * @return UV coordinates for each vertex
 */
Eigen::MatrixXd
lscm(
    Eigen::Ref<const compas::RowMatrixXd> V,
    Eigen::Ref<const compas::RowMatrixXi> F);
