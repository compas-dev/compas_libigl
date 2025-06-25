#pragma once

#include "compas.hpp"
#include <igl/isolines.h>
#include <Eigen/Core>

namespace compas_libigl {

/**
 * Compute isolines on a triangle mesh.
 *
 * @param V The vertex matrix of the triangle mesh (n x 3).
 * @param F The face matrix of the triangle mesh (m x 3).
 * @param isovalues The scalar values per vertex (n x 1).
 * @param vals The isovalues at which to compute isolines.
 * @return Tuple of (vertices, edges, indices) defining the isolines.
 */
compas::IsolinesResult trimesh_isolines(
    Eigen::Ref<const compas::RowMatrixXd> V,
    Eigen::Ref<const compas::RowMatrixXi> F,
    Eigen::Ref<const Eigen::VectorXd> isovalues,
    Eigen::Ref<const Eigen::VectorXd> vals
);

} // namespace compas_libigl
