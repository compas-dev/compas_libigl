#pragma once

#include "compas.hpp"
#include <igl/ramer_douglas_peucker.h>
#include <Eigen/Core>

/**
 * Simplify a polyline using Ramer-Douglas-Peucker algorithm.
 *
 * @param P #P x 3 matrix of polyline points
 * @param threshold Maximum distance threshold for simplification
 * @return Tuple of (simplified points, indices of kept points, mapping from simplified to original)
 */
std::tuple<compas::RowMatrixXd, Eigen::VectorXi, Eigen::VectorXi>
ramer_douglas_peucker(
    Eigen::Ref<const compas::RowMatrixXd> P,
    double threshold);
