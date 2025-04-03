#pragma once

#include "compas.hpp"
#include <igl/isolines.h>
#include <Eigen/Core>

/**
 * Compute isolines on a triangle mesh.
 *
 * @param V The vertex matrix of the triangle mesh (n x 3).
 * @param F The face matrix of the triangle mesh (m x 3).
 * @param isovalues The scalar values per vertex (n x 1).
 * @param vals The isovalues at which to compute isolines.
 * @return Tuple of (vertices, edges, indices) defining the isolines.
 */
std::tuple<compas::RowMatrixXd, compas::RowMatrixXi, compas::RowMatrixXi>
trimesh_isolines(
    const compas::RowMatrixXd V,
    const compas::RowMatrixXi F,
    const Eigen::VectorXd isovalues,
    const Eigen::VectorXd vals
);