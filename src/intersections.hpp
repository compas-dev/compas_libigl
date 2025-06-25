#pragma once

#include "compas.hpp"
#include <igl/ray_mesh_intersect.h>
#include <igl/Hit.h>
#include <Eigen/Core>

/**
 * Compute intersection between a single ray and a mesh.
 * 
 * @param point Origin point of the ray
 * @param direction Direction vector of the ray
 * @param V #V x 3 matrix of vertex coordinates
 * @param F #F x 3 matrix of triangle indices
 * @return Vector of intersection hits, each containing (face_id, u, v, t) where:
 *         - face_id: index of intersected face
 *         - u, v: barycentric coordinates of hit point
 *         - t: ray parameter at intersection
 */
 compas::VectorTupleIntFloatFloatFloat intersection_ray_mesh(
    const Eigen::Vector3d& point, 
    const Eigen::Vector3d& direction,
    Eigen::Ref<const compas::RowMatrixXd> V, 
    Eigen::Ref<const compas::RowMatrixXi> F);

/**
 * Compute intersections between multiple rays and a mesh.
 * 
 * @param points #R x 3 matrix of ray origin points
 * @param directions #R x 3 matrix of ray direction vectors
 * @param V #V x 3 matrix of vertex coordinates
 * @param F #F x 3 matrix of triangle indices
 * @return Vector of intersection hits per ray, each hit containing (face_id, u, v, t)
 */
compas::VectorVectorTupleIntFloatFloatFloat intersection_rays_mesh(
    Eigen::Ref<const compas::RowMatrixXd> points,
    Eigen::Ref<const compas::RowMatrixXd> directions,
    Eigen::Ref<const compas::RowMatrixXd> V, 
    Eigen::Ref<const compas::RowMatrixXi> F);
