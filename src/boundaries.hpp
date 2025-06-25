#pragma once

#include "compas.hpp"
#include <igl/boundary_loop.h>

/**
 * Compute all ordered boundary loops of a manifold triangle mesh.
 *
 * @param F The face matrix of the triangle mesh (n x 3).
 * @return A vector of vectors containing vertex indices for each boundary loop.
 *
 * @note The input mesh should be manifold for correct results.
 */
 compas::VectorVectorInt trimesh_boundaries(Eigen::Ref<const compas::RowMatrixXi> F);