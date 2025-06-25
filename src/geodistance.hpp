#pragma once

#include "compas.hpp"
#include <Eigen/Core>
#include <igl/avg_edge_length.h>
#include <igl/exact_geodesic.h>
#include <igl/heat_geodesics.h>

/**
 * Helper function to compute exact geodesic distances.
 */
compas::VectorXd trimesh_geodistance_exact(
    const compas::RowMatrixXd& V,
    const compas::RowMatrixXi& F,
    int vid);

/**
 * Helper function to compute heat method geodesic distances.
 */
compas::VectorXd trimesh_geodistance_heat(
    const compas::RowMatrixXd& V,
    const compas::RowMatrixXi& F,
    int vid);

/**
 * Compute geodesic distance from a source vertex to all other vertices.
 *
 * @param V The vertex matrix of the triangle mesh (n x 3).
 * @param F The face matrix of the triangle mesh (m x 3).
 * @param source Index of the source vertex.
 * @param method Method to use: "exact" or "heat".
 * @return Vector of geodesic distances from source to all vertices.
 */
compas::VectorXd trimesh_geodistance(
    Eigen::Ref<const compas::RowMatrixXd> V,
    Eigen::Ref<const compas::RowMatrixXi> F,
    int source,
    const std::string& method
);

/**
 * Compute geodesic distance from multiple source vertices.
 *
 * @param V The vertex matrix of the triangle mesh (n x 3).
 * @param F The face matrix of the triangle mesh (m x 3).
 * @param sources Vector of source vertex indices.
 * @param method Method to use: "exact" or "heat".
 * @return Vector of minimum geodesic distances from any source to all vertices.
 */
compas::VectorXd trimesh_geodistance_multiple(
    Eigen::Ref<const compas::RowMatrixXd> V,
    Eigen::Ref<const compas::RowMatrixXi> F,
    Eigen::Ref<const compas::VectorXi> sources,
    const std::string& method
);