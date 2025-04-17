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

// Private methods

void cleanMesh(
    const compas::RowMatrixXd& V_in, 
    const compas::RowMatrixXi& F_in, 
    std::vector<std::vector<int>>& faces_);

void getTriFace(
    const compas::RowMatrixXi& F_, 
    int faceID, 
    const compas::RowMatrixXd& V, 
    compas::RowMatrixXd& A, 
    compas::RowMatrixXd& B, 
    compas::RowMatrixXd& C);

bool mapPoint3D_simple(
    const compas::RowMatrixXi& F_, 
    const compas::RowMatrixXd& UV_, 
    const Eigen::Vector3d& pt, 
    Eigen::Vector3d& barycentric, 
    int& faceID);

    // Eigen::Ref<const compas::RowMatrixXd> V,
    // Eigen::Ref<const compas::RowMatrixXi> F)

void mapMesh3D_AABB(
    Eigen::Ref<const compas::RowMatrixXd> v, 
    Eigen::Ref<const compas::RowMatrixXi> f, 
    Eigen::Ref<const compas::RowMatrixXd> uv,
    Eigen::Ref<compas::RowMatrixXd>  pattern_v, 
    Eigen::Ref<const compas::RowMatrixXi> pattern_f, 
    Eigen::Ref<const compas::RowMatrixXd> pattern_uv, 
    std::vector<std::vector<int>>& pattern_polygonal_faces);


class iglMesh {
    public:
    
        compas::RowMatrixXd V_;
    
        std::vector<std::vector<int>> faces_; //polygonal Mesh
        compas::RowMatrixXi F_; //triangle Mesh
    
        compas::RowMatrixXd UV_; //uv
    public:
    
        iglMesh(){};
    
    public:
    
        void mapMesh3D_simple(iglMesh &baseMesh);
    
        
    
       
    
    
    private:
        
    
        
    };


// namespace nb = nanobind;

// // Helper function to get triangle vertices at a specific face index
// void getTriFace(
//     const Eigen::Ref<const compas::RowMatrixXd> V,
//     const Eigen::Ref<const compas::RowMatrixXi> F,
//     int faceID,
//     Eigen::Ref<const compas::RowMatrixXd> A,
//     Eigen::Ref<const compas::RowMatrixXd> B,
//     Eigen::Ref<const compas::RowMatrixXd> C);

// // Map a single point to a mesh using barycentric coordinates
// bool mapPoint3D_simple(
//     const Eigen::RowVector3d& pt, 
//     const Eigen::Ref<const compas::RowMatrixXd> V_uv,
//     const Eigen::Ref<const compas::RowMatrixXi> F,
//     Eigen::RowVector3d& l, 
//     int& faceID);
