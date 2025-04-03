#pragma once

#include "compas.hpp"
#include <igl/avg_edge_length.h>
#include <igl/exact_geodesic.h>
#include <igl/heat_geodesics.h>

/**
 * Compute geodesic distance from a source vertex to all other vertices.
 *
 * @param V The vertex matrix of the triangle mesh (n x 3).
 * @param F The face matrix of the triangle mesh (m x 3).
 * @param source Index of the source vertex.
 * @param method Method to use: "exact" or "heat".
 * @return Vector of geodesic distances from source to all vertices.
 */
Eigen::VectorXd trimesh_geodistance(
    compas::RowMatrixXd V,
    compas::RowMatrixXi F,
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
Eigen::VectorXd trimesh_geodistance_multiple(
    compas::RowMatrixXd V,
    compas::RowMatrixXi F,
    Eigen::VectorXi sources,
    const std::string& method
);