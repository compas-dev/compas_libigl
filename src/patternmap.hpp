#pragma once

#include "compas.hpp"

#include <Eigen/Dense>

// #include <igl/polygon_mesh_to_triangle_mesh.h>
#include <igl/polygons_to_triangles.h>
#include <igl/remove_duplicate_vertices.h>
#include <igl/barycentric_coordinates.h>
#include <igl/lscm.h>
#include <igl/boundary_loop.h>
#include <igl/AABB.h>
#include <igl/edges.h>

class iglMesh {
public:

    Eigen::MatrixXd V_;

    std::vector<std::vector<int>> faces_; //polygonal Mesh
    Eigen::MatrixXi F_; //triangle Mesh

    Eigen::MatrixXd UV_; //uv
public:

    iglMesh(){};

    void loadMesh(std::vector<std::vector<double>> &_vertices, std::vector<std::vector<int>>& _faces);

    std::vector<std::vector<double>> getVertices();

    std::vector<std::vector<double>> getUVs();

    std::vector<std::vector<int>> getFaces();

public:

    void parametrization_simple();

    void parametrization_lscm();

    void mapMesh3D_simple(iglMesh &baseMesh);

    bool mapPoint3D_simple(Eigen::Vector3d pt, Eigen::Vector3d &barycentric, int &faceID);

    void mapMesh3D_AABB(iglMesh &baseMesh);


private:

    void cleanMesh();

    void getTriFace(int faceID, Eigen::MatrixXd &V, Eigen::MatrixXd &A, Eigen::MatrixXd &B, Eigen::MatrixXd &C);
};