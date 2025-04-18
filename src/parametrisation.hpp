#pragma once

#include "compas.hpp"
#include <Eigen/Core>

/**
 * Rescale UV coordinates to fit in a 0-1 box while maintaining aspect ratio.
 * 
 * @param V_uv #V x 2 matrix of UV coordinates
 */
void rescale(Eigen::MatrixXd &V_uv);

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
