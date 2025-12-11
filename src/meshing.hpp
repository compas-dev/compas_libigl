#pragma once

#include "compas.hpp"
#include <Eigen/Core>
#include <Eigen/Sparse>
#include <igl/cut_mesh.h>
#include <igl/facet_components.h>
#include <igl/remesh_along_isoline.h>

/**
 * Remesh a triangle mesh along an isoline.
 *
 * @param V1 #V x 3 matrix of vertex coordinates
 * @param F1 #F x 3 matrix of triangle indices
 * @param S1 #V x 1 vector of scalar values
 * @param s Isovalue at which to cut
 * @return Tuple of (vertices, faces, labels) where labels indicate which side of the cut each face is on
 */
std::tuple<compas::RowMatrixXd, compas::RowMatrixXi, Eigen::VectorXi>
trimesh_remesh_along_isoline(
    Eigen::Ref<const compas::RowMatrixXd> V1,
    Eigen::Ref<const compas::RowMatrixXi> F1,
    Eigen::Ref<const Eigen::VectorXd> S1,
    double s);

/**
 * Remesh a triangle mesh along multiple isolines.
 *
 * @param V_initial #V x 3 matrix of vertex coordinates
 * @param F_initial #F x 3 matrix of triangle indices
 * @param S_initial #V x 1 vector of scalar values
 * @param values Vector of isovalues at which to cut
 * @return Tuple of (vertices, faces, scalar values, face groups) where face groups indicate regions between cuts
 */
std::tuple<compas::RowMatrixXd, compas::RowMatrixXi, Eigen::VectorXd, Eigen::VectorXi>
trimesh_remesh_along_isolines(
    Eigen::Ref<const compas::RowMatrixXd> V_initial,
    Eigen::Ref<const compas::RowMatrixXi> F_initial,
    Eigen::Ref<const Eigen::VectorXd> S_initial,
    Eigen::Ref<const Eigen::VectorXd> values);

/**
 * Cut a mesh along specified edges.
 *
 * @param V #V x 3 matrix of vertex coordinates
 * @param F #F x 3 matrix of triangle indices
 * @param cuts #F x 3 matrix of boolean cut flags per edge
 * @return Tuple of (vertices, faces) with vertices duplicated along cuts
 */
std::tuple<compas::RowMatrixXd, compas::RowMatrixXi>
trimesh_cut_mesh(
    Eigen::Ref<const compas::RowMatrixXd> V,
    Eigen::Ref<const compas::RowMatrixXi> F,
    Eigen::Ref<const compas::RowMatrixXi> cuts);

/**
 * Compute connected components of mesh faces.
 *
 * @param F #F x 3 matrix of triangle indices
 * @return Vector of component IDs per face
 */
Eigen::VectorXi
trimesh_face_components(
    Eigen::Ref<const compas::RowMatrixXi> F);
