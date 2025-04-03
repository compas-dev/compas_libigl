#pragma once

#include "compas.hpp"
#include <igl/massmatrix.h>
#include <Eigen/Core>

/**
 * Compute the mass matrix of a triangle mesh.
 *
 * @param V The vertex matrix of the triangle mesh (n x 3).
 * @param F The face matrix of the triangle mesh (m x 3).
 * @return Vector of mass values per vertex.
 */
Eigen::VectorXd trimesh_massmatrix(
    compas::RowMatrixXd V,
    compas::RowMatrixXi F
);