#pragma once

#include "compas.hpp"
#include <igl/polygons_to_triangles.h>
#include <igl/remove_duplicate_vertices.h>
#include <igl/barycentric_coordinates.h>
#include <igl/lscm.h>
#include <igl/boundary_loop.h>
#include <igl/AABB.h>
#include <igl/edges.h>
#include <Eigen/Core>
#include <clipper2/clipper.h>
#include <igl/boundary_loop.h>
#include <igl/per_vertex_normals.h>
#include <igl/adjacency_list.h>

/**
 * Map a 2D already croppedpattern mesh onto a 3D target mesh using AABB tree-based mapping.
 * This function maps each vertex of the pattern mesh to the target mesh using
 * barycentric interpolation based on the UV parameterization of the target mesh.
 * Computes normal vectors through barycentric interpolation.
 *
 * @param v The vertex matrix of the target mesh.
 * @param f The face matrix of the target mesh.
 * @param uv The UV coordinates of the target mesh.
 * @param pattern_v The vertex matrix of the pattern mesh to be mapped.
 * @param pattern_f The face vector of vectors of int.
 * @param pattern_uv The UV coordinates of the pattern mesh.
 * @param pattern_normals Output matrix for interpolated normal vectors.
 * @return Vector of vectors representing the polygonal faces of the mapped pattern mesh.
 */
compas::VectorVectorInt map_mesh_cropped(
    Eigen::Ref<const compas::RowMatrixXd> v, 
    Eigen::Ref<const compas::RowMatrixXi> f, 
    Eigen::Ref<const compas::RowMatrixXd> uv,
    Eigen::Ref<compas::RowMatrixXd> pattern_v, 
    const compas::VectorVectorInt& pattern_f, 
    Eigen::Ref<const compas::RowMatrixXd> pattern_uv,
    Eigen::Ref<compas::RowMatrixXd> pattern_normals);

/**
 * Check if two paths intersect.
 *
 * @param path1 The first path.
 * @param path2 The second path.
 * @param scale The scale factor for the paths.
 * @return True if the paths intersect, false otherwise.
 */
bool path_intersect(const Clipper2Lib::PathD& path1, const Clipper2Lib::PathD& path2, double scale = 1e6);

/**
 * Check if two paths intersect.
 *
 * @param paths1 The first path.
 * @param paths2 The second path.
 * @param scale The scale factor for the paths.
 * @return True if the paths intersect, false otherwise.
 */
bool paths_intersect(const Clipper2Lib::PathsD& paths1, const Clipper2Lib::PathsD& paths2, double scale = 1e6);

/**
 * Convert Eigen mesh to Clipper paths.
 *
 * @param flattned_target_uv The flattened target UV coordinates.
 * @param target_f The target mesh face indices.
 * @param pattern_v The pattern mesh vertex coordinates.
 * @param pattern_f The pattern mesh face indices.
 * @param clip_boundaries Whether to clip the pattern mesh to the boundaries of the target mesh.
 * @param simplify_borders Whether to simplify the border of the pattern mesh.
 * @param fixed_vertices fixed points on the target mesh
 * @param tolerance The tolerance for point comparison, to remove duplicates.
 * @return A tuple of the clipped pattern mesh vertex coordinates and face indices.
 */
std::tuple<compas::RowMatrixXd, std::vector<std::vector<int>>, std::vector<bool>, std::vector<int>> eigen_to_clipper (
    Eigen::Ref<const compas::RowMatrixXd> flattned_target_uv,
    Eigen::Ref<const compas::RowMatrixXi> target_f, 
    
    Eigen::Ref<const compas::RowMatrixXd> pattern_v, 
    const std::vector<std::vector<int>>& pattern_f,
    bool clip_boundaries,
    bool simplify_borders,
    std::vector<int>& fixed_vertices,
    double tolerance = 1e-6
)  ;    

/**
 * Map a 2D pattern mesh onto a 3D target mesh with automatic parameterization, mesh is always mapped to 1x1 unit.
 * This function automatically computes the UV parameterization for both meshes
 * and then performs mapping, eliminating the need for separate parameterization steps.
 * 
 * @param target_v #V x 3 matrix of target mesh vertex coordinates
 * @param target_f #F x 3 matrix of target mesh triangle indices
 * @param pattern_v #V x 3 matrix of pattern mesh vertex coordinates
 * @param pattern_f vector of vectors of int of pattern mesh triangle indices
 * @param clip_boundaries whether to clip the pattern mesh to the boundaries of the target mesh
 * @param simplify_borders whether to simplify the border of the pattern mesh
 * @param fixed_vertices fixed points on the target mesh
 * @param tolerance tolerance for point comparison, to remove duplicates
 * @return A tuple containing the mapped pattern vertices, faces, and vertex normal vectors.
 */
compas::MeshMapResult map_mesh_with_automatic_parameterization(
    Eigen::Ref<const compas::RowMatrixXd> target_v, 
    Eigen::Ref<const compas::RowMatrixXi> target_f, 
    Eigen::Ref<compas::RowMatrixXd> pattern_v, 
    const compas::VectorVectorInt& pattern_f,
    bool clip_boundaries,
    bool simplify_borders,
    compas::VectorInt& fixed_vertices,
    double tolerance = 1e-6
);