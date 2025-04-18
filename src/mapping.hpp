#pragma once

#include "compas.hpp"
#include <igl/polygons_to_triangles.h>
#include <igl/remove_duplicate_vertices.h>
#include <igl/barycentric_coordinates.h>
#include <igl/lscm.h>
#include <igl/boundary_loop.h>
#include <igl/AABB.h>
#include <igl/edges.h>
#include <algorithm>
#include <Eigen/Core>

/**
 * Helper function to extract triangle vertices at a specific face index.
 *
 * @param F_ The face matrix of the triangle mesh.
 * @param faceID Index of the face to extract.
 * @param V The vertex matrix.
 * @param A Output parameter for the first vertex of the triangle.
 * @param B Output parameter for the second vertex of the triangle.
 * @param C Output parameter for the third vertex of the triangle.
 */
void get_triface(
    const compas::RowMatrixXi& F_, 
    int faceID, 
    const compas::RowMatrixXd& V, 
    compas::RowMatrixXd& A, 
    compas::RowMatrixXd& B, 
    compas::RowMatrixXd& C);

/**
 * Map a point to a mesh using barycentric coordinates.
 *
 * @param F_ The face matrix of the triangle mesh.
 * @param UV_ The UV coordinates matrix.
 * @param pt The 3D point to map.
 * @param barycentric Output parameter for the barycentric coordinates.
 * @param faceID Output parameter for the face index.
 * @return True if the point was successfully mapped, false otherwise.
 */
bool map_point3d_simple(
    const compas::RowMatrixXi& F_, 
    const compas::RowMatrixXd& UV_, 
    const Eigen::Vector3d& pt, 
    Eigen::Vector3d& barycentric, 
    int& faceID);

/**
 * Map a 2D pattern mesh onto a 3D target mesh using AABB tree-based mapping.
 * This function maps each vertex of the pattern mesh to the target mesh using
 * barycentric interpolation based on the UV parameterization of the target mesh.
 *
 * @param v The vertex matrix of the target mesh.
 * @param f The face matrix of the target mesh.
 * @param uv The UV coordinates of the target mesh.
 * @param pattern_v The vertex matrix of the pattern mesh to be mapped.
 * @param pattern_f The face vector of vectors of int.
 * @param pattern_uv The UV coordinates of the pattern mesh.
 * @return Vector of vectors representing the polygonal faces of the mapped pattern mesh.
 */
std::vector<std::vector<int>> map_mesh(
    Eigen::Ref<const compas::RowMatrixXd> v, 
    Eigen::Ref<const compas::RowMatrixXi> f, 
    Eigen::Ref<const compas::RowMatrixXd> uv,
    Eigen::Ref<compas::RowMatrixXd> pattern_v, 
    const std::vector<std::vector<int>>& pattern_f  , 
    Eigen::Ref<const compas::RowMatrixXd> pattern_uv);


/**
 * Map a 2D pattern mesh onto a 3D target mesh with automatic parameterization, mesh is always mapped to 1x1 unit.
 * This function automatically computes the UV parameterization for both meshes
 * and then performs mapping, eliminating the need for separate parameterization steps.
 * 
 * @param target_v #V x 3 matrix of target mesh vertex coordinates
 * @param target_f #F x 3 matrix of target mesh triangle indices
 * @param pattern_v #V x 3 matrix of pattern mesh vertex coordinates
 * @param pattern_f vector of vectors of int of pattern mesh triangle indices
 * @return A vector of face indices representing polygons in the mapped mesh
 */
std::vector<std::vector<int>> map_mesh_with_automatic_parameterization(
    Eigen::Ref<const compas::RowMatrixXd> target_v, 
    Eigen::Ref<const compas::RowMatrixXi> target_f, 
    Eigen::Ref<compas::RowMatrixXd> pattern_v, 
    const std::vector<std::vector<int>>& pattern_f);