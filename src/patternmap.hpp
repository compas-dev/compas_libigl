#pragma once

#include "compas.hpp"

#include <Eigen/Dense>
#include <vector>
#include <iostream>

// #include <igl/polygon_mesh_to_triangle_mesh.h>
#include <igl/polygons_to_triangles.h>
#include <igl/remove_duplicate_vertices.h>
#include <igl/barycentric_coordinates.h>
#include <igl/lscm.h>
#include <igl/boundary_loop.h>
#include <igl/AABB.h>
#include <igl/edges.h>
#include <algorithm>

using std::vector;
using Eigen::MatrixXd;
using Eigen::MatrixXi;
using Eigen::Vector3d;

class iglMesh {
public:

    MatrixXd V_;

    vector<vector<int>> faces_; //polygonal Mesh
    MatrixXi F_; //triangle Mesh

    MatrixXd UV_; //uv
public:

    iglMesh(){};

    void loadMesh(vector<vector<double>> &_vertices, vector<vector<int>>& _faces);

    vector<vector<double>> getVertices();

    vector<vector<double>> getUVs();

    vector<vector<int>> getFaces();

public:

    void parametrization_simple();

    void parametrization_lscm();

    void mapMesh3D_simple(iglMesh &baseMesh);

    bool mapPoint3D_simple(Eigen::Vector3d pt, Eigen::Vector3d &barycentric, int &faceID);

    void mapMesh3D_AABB(iglMesh &baseMesh);

public:

    iglMesh saveWireFrame(double thickness, int cylinder_pts);

private:

    void cleanMesh();

    void getTriFace(int faceID, Eigen::MatrixXd &V, Eigen::MatrixXd &A, Eigen::MatrixXd &B, Eigen::MatrixXd &C);
};