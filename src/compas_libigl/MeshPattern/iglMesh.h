//
// Created by ziqwang on 2019-04-13.
//

#ifndef COMPAS_LIBIGL_IGLMESH_H
#define COMPAS_LIBIGL_IGLMESH_H

#include <eigen3/Eigen/Dense>
#include <vector>
#include <iostream>

using std::vector;
using Eigen::MatrixXd;
using Eigen::MatrixXi;

class iglMesh {
public:

    MatrixXd V_;

    vector<vector<int>> faces_; //polygonal Mesh
    MatrixXi F_; //triangle Mesh

public:

    iglMesh(){};

    void loadMesh(vector<vector<double>> &_vertices, vector<vector<int>>& _faces);

    vector<vector<double>> getVertices();

    vector<vector<int>> getFaces();

public:

    void make_flat();
};


#endif //COMPAS_LIBIGL_IGLMESH_H
