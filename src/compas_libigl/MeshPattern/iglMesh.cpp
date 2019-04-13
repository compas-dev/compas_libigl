//
// Created by ziqwang on 2019-04-13.
//

#include "iglMesh.h"
#include <igl/polygon_mesh_to_triangle_mesh.h>
#include <igl/remove_duplicate_vertices.h>

void iglMesh::loadMesh(vector<vector<double>> &_vertices, vector<vector<int>> &_faces)
{
    //read vertices' coordinates
    V_ = Eigen::MatrixXd::Zero(_vertices.size() , 3);
    for(int id = 0; id < _vertices.size(); id++)
    {
        V_.row(id) = Eigen::RowVector3d(_vertices[id][0], _vertices[id][1], _vertices[id][2]);
    }


    //read faces
    faces_ = _faces;
    igl::polygon_mesh_to_triangle_mesh(faces_, F_);

    //remove duplicate
    MatrixXd SV;
    MatrixXi SF;
    Eigen::VectorXi SVI, SVJ;
    igl::remove_duplicate_vertices(V_, F_, 1e-6f, SV, SVI, SVJ, SF);
    F_ = SF;
    V_ = SV;

    for(int id = 0;id < faces_.size(); ++id)
    {
        for(int jd = 0; jd < faces_[id].size(); ++jd)
        {
            faces_[id][jd] = SVJ(faces_[id][jd]);
        }
    }
}

vector<vector<double>> iglMesh::getVertices()
{
    //write vertices
    vector<vector<double>> vertices;
    for(int id = 0; id < V_.rows(); id++){
        vector<double> pos;
        pos.push_back(V_(id, 0));pos.push_back(V_(id, 1));pos.push_back(V_(id, 2));
        vertices.push_back(pos);
    }
    return vertices;
}

vector<vector<int>> iglMesh::getFaces() {
    return faces_;
}


void iglMesh::make_flat()
{
    V_.col(2) = Eigen::VectorXd::Zero(V_.rows());
}

