#pragma once

#include "compas.hpp"
#include <igl/boundary_loop.h>
#include <igl/harmonic.h>
#include <igl/lscm.h>
#include <igl/map_vertices_to_circle.h>
#include <Eigen/Core>

/**
 * Compute harmonic parametrization of a triangle mesh.
 *
 * @param V The vertex matrix of the triangle mesh (n x 3).
 * @param F The face matrix of the triangle mesh (m x 3).
 * @param bnd The boundary vertex indices.
 * @param bnd_uv The UV coordinates for boundary vertices.
 * @param harmonic_order The order of harmonic weights (1: harmonic, 2: biharmonic).
 * @return Matrix of UV coordinates for all vertices.
 */
Eigen::MatrixXd trimesh_harmonic_parametrisation(
    const Eigen::MatrixXd& V,
    const Eigen::MatrixXi& F,
    const Eigen::VectorXi& bnd,
    const Eigen::MatrixXd& bnd_uv,
    const int harmonic_order
);