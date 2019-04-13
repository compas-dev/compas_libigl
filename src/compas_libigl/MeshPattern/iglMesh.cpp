//
// Created by ziqwang on 2019-04-13.
//

#include "iglMesh.h"
#include <igl/polygon_mesh_to_triangle_mesh.h>
#include <igl/remove_duplicate_vertices.h>
#include <igl/barycentric_coordinates.h>
#include <igl/lscm.h>
#include <igl/boundary_loop.h>
#include <igl/AABB.h>

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

    cleanMesh();
}

void iglMesh::cleanMesh()
{
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

vector<vector<double>> iglMesh::getUVs()
{
    //write vertices
    vector<vector<double>> uvs;
    for(int id = 0; id < UV_.rows(); id++){
        vector<double> pos;
        pos.push_back(UV_(id, 0));pos.push_back(UV_(id, 1)); pos.push_back(0);
        uvs.push_back(pos);
    }
    return uvs;
}



void iglMesh::paramertization_simple()
{
    UV_.setZero();

    UV_ = V_.leftCols(2);
    Eigen::Vector2d min_coeff, max_coeff;
    min_coeff = UV_.colwise().minCoeff();
    max_coeff = UV_.colwise().maxCoeff();
    for(int id = 0; id < UV_.rows(); id++)
    {
        UV_(id, 0) = (UV_(id, 0) - min_coeff(0)) / (max_coeff(0) - min_coeff(0));
        UV_(id, 1) = (UV_(id, 1) - min_coeff(1)) / (max_coeff(1) - min_coeff(1));
    }
}

void iglMesh::paramertization_lscm()
{
    UV_.setZero();

    Eigen::VectorXi bnd,b(2,1);
    igl::boundary_loop(F_,bnd);
    b(0) = bnd(0);
    b(1) = bnd(round(bnd.size()/2));
    MatrixXd bc(2,2);
    bc<<0,0,1,0;
    igl::lscm(V_,F_,b,bc,UV_);

    Eigen::Vector2d min_coeff, max_coeff;
    min_coeff = UV_.colwise().minCoeff();
    max_coeff = UV_.colwise().maxCoeff();
    for(int id = 0; id < UV_.rows(); id++)
    {
        UV_(id, 0) = (UV_(id, 0) - min_coeff(0));
        UV_(id, 1) = (UV_(id, 1) - min_coeff(1));
    }
    return;
}

bool iglMesh::mapPoint3D_simple(Eigen::Vector3d pt, Eigen::Vector3d &l, int &faceID)
{
    if(UV_.isZero())
    {
        return false;
    }
    else{
        Eigen::MatrixXd P(1, 3), L(1, 3);
        P << pt(0), pt(1), pt(2);
        for(int id = 0; id < F_.rows(); id++)
        {
            Eigen::MatrixXd A, B, C;
            getTriFace(id, UV_, A, B, C);
            igl::barycentric_coordinates(P, A, B, C, L);
            if(L.minCoeff() < -1e-5 || L.maxCoeff() > 1 + 1e-5){
                continue;
            }
            else{
                l = L.row(0);
                faceID = id;
                return true;
            }
        }
    }

    return false;
}

void iglMesh::mapMesh3D_simple(iglMesh &baseMesh)
{
    if(UV_.isZero()){
        paramertization_simple();
    }

    vector<int> ref_faceIDs;
    for(int id = 0; id < baseMesh.V_.rows(); id++)
    {
        Eigen::Vector3d pt = baseMesh.V_.row(id);
        Eigen::Vector3d l(0, 0, 0);
        int faceID = -1;
        if(mapPoint3D_simple(pt, l, faceID))
        {
            Eigen::MatrixXd A, B, C;
            getTriFace(faceID, V_, A, B, C);
            baseMesh.V_.row(id) = A.row(0) * l(0) + B.row(0) * l(1) + C.row(0) * l(2);
            ref_faceIDs.push_back(faceID);
        }
        else{
            ref_faceIDs.push_back(-1);
        }
    }

    for(auto it = baseMesh.faces_.begin(); it != baseMesh.faces_.end();)
    {
        bool all_in_refMesh = true;
        for(int jd = 0; jd < (*it).size(); jd++)
        {
            int fid = (*it)[jd];
            if(ref_faceIDs[fid] == -1){
                all_in_refMesh = false;
                break;
            }
        }
        if(!all_in_refMesh){
            it = baseMesh.faces_.erase(it);
        }
        else{
            it++;
        }
    }

    baseMesh.cleanMesh();
}

void iglMesh::mapMesh3D_AABB(iglMesh &baseMesh)
{
    if(UV_.isZero()){
        paramertization_lscm();
    }

    igl::AABB<MatrixXd, 2> tree;
    tree.init(UV_, F_);

    vector<int> ref_faceIDs;
    baseMesh.paramertization_simple();
    MatrixXd C;
    Eigen::VectorXi I;
    Eigen::VectorXd sqrD;
    tree.squared_distance(UV_, F_, baseMesh.UV_, sqrD, I, C);
    for(int id = 0; id < baseMesh.UV_.rows(); id++)
    {
        if(std::fabs(sqrD[id]) < 1e-5)
        {
            Eigen::MatrixXd A, B, C, L, P(1, 3);
            P << baseMesh.UV_(id, 0), baseMesh.UV_(id, 1), 0;
            getTriFace(I(id), UV_, A, B, C);
            igl::barycentric_coordinates(P, A, B, C, L);

            ref_faceIDs.push_back(I(id));
            getTriFace(I(id), V_, A, B, C);
            baseMesh.V_.row(id) = A.row(0) * L(0, 0) + B.row(0) * L(0, 1) + C.row(0) * L(0, 2);
        }
        else{
            ref_faceIDs.push_back(-1);
        }
    }

    for(auto it = baseMesh.faces_.begin(); it != baseMesh.faces_.end();)
    {
        bool all_in_refMesh = true;
        for(int jd = 0; jd < (*it).size(); jd++)
        {
            int fid = (*it)[jd];
            if(ref_faceIDs[fid] == -1){
                all_in_refMesh = false;
                break;
            }
        }
        if(!all_in_refMesh){
            it = baseMesh.faces_.erase(it);
        }
        else{
            it++;
        }
    }
    baseMesh.cleanMesh();
}


void iglMesh::getTriFace(int faceID, Eigen::MatrixXd &V, Eigen::MatrixXd &A, Eigen::MatrixXd &B, Eigen::MatrixXd &C)
{
    if(0 <= faceID && faceID < F_.rows())
    {
        A = MatrixXd(1, 3);
        B = MatrixXd(1, 3);
        C = MatrixXd(1, 3);
        if(V.cols() == 2)
        {
            A << V(F_(faceID, 0), 0), V(F_(faceID, 0), 1), 0;
            B << V(F_(faceID, 1), 0), V(F_(faceID, 1), 1), 0;
            C << V(F_(faceID, 2), 0), V(F_(faceID, 2), 1), 0;
        }
        else if(V.cols() == 3){
            A << V(F_(faceID, 0), 0), V(F_(faceID, 0), 1), V(F_(faceID, 0), 2);
            B << V(F_(faceID, 1), 0), V(F_(faceID, 1), 1), V(F_(faceID, 0), 2);
            C << V(F_(faceID, 2), 0), V(F_(faceID, 2), 1), V(F_(faceID, 0), 2);
        }
    }

    return;
}







