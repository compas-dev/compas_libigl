#include "mapping.hpp"


void get_triface(
    const compas::RowMatrixXi& F_,
    int faceID, 
    const compas::RowMatrixXd& V, 
    compas::RowMatrixXd& A, 
    compas::RowMatrixXd& B, 
    compas::RowMatrixXd& C)
{
    if(0 <= faceID && faceID < F_.rows())
    {
        A = compas::RowMatrixXd(1, 3);
        B = compas::RowMatrixXd(1, 3);
        C = compas::RowMatrixXd(1, 3);
        if(V.cols() == 2)
        {
            A << V(F_(faceID, 0), 0), V(F_(faceID, 0), 1), 0;
            B << V(F_(faceID, 1), 0), V(F_(faceID, 1), 1), 0;
            C << V(F_(faceID, 2), 0), V(F_(faceID, 2), 1), 0;
        }
        else if(V.cols() == 3){
            A << V(F_(faceID, 0), 0), V(F_(faceID, 0), 1), V(F_(faceID, 0), 2);
            B << V(F_(faceID, 1), 0), V(F_(faceID, 1), 1), V(F_(faceID, 1), 2);
            C << V(F_(faceID, 2), 0), V(F_(faceID, 2), 1), V(F_(faceID, 2), 2);
        }
    }

    return;
}

bool map_point3d_simple(
    const compas::RowMatrixXi& F_, 
    const compas::RowMatrixXd& UV_, 
    const Eigen::Vector3d& pt, 
    Eigen::Vector3d& l, 
    int& faceID)
{
    if(UV_.isZero())
    {
        return false;
    }
    else{
        compas::RowMatrixXd P(1, 3), L(1, 3);
        P << pt(0), pt(1), pt(2);
        for(int id = 0; id < F_.rows(); id++)
        {
            compas::RowMatrixXd A, B, C;
            get_triface(F_, id, UV_, A, B, C);
            igl::barycentric_coordinates(P, A, B, C, L);
            if(L.minCoeff() < -1e-5 || L.maxCoeff() > 1 + 1e-5){
                continue;
            }
            else{
                l = Eigen::Vector3d(L(0, 0), L(0, 1), L(0, 2));
                faceID = id;
                return true;
            }
        }
    }

    return false;
}

std::vector<std::vector<int>> map_mesh(
    Eigen::Ref<const compas::RowMatrixXd> v, 
    Eigen::Ref<const compas::RowMatrixXi> f, 
    Eigen::Ref<const compas::RowMatrixXd> uv,
    
    Eigen::Ref<compas::RowMatrixXd> pattern_v, 
    const std::vector<std::vector<int>>& pattern_f, 
    Eigen::Ref<const compas::RowMatrixXd> pattern_uv)
{

    // Use regular MatrixXd to avoid type conflicts with AABB functions
    Eigen::MatrixXd V_uv = uv;
    Eigen::MatrixXi F_faces = f;
    
    igl::AABB<Eigen::MatrixXd, 2> tree;
    tree.init(V_uv, F_faces);

    std::vector<bool> inMesh;
    Eigen::MatrixXd C;
    Eigen::VectorXi I;
    Eigen::VectorXd sqrD;
    Eigen::MatrixXd pattern_uv_eigen = pattern_uv;
    
    tree.squared_distance(V_uv, F_faces, pattern_uv_eigen, sqrD, I, C);
    
    for(int id = 0; id < pattern_uv.rows(); id++)
    {
        if(std::fabs(sqrD[id]) < 1e-5) // Tolerance
        {
            compas::RowMatrixXd A, B, C;
            Eigen::MatrixXd P(1, 3);
            P << pattern_uv(id, 0), pattern_uv(id, 1), 0;
            compas::RowMatrixXd UV_A, UV_B, UV_C;
            get_triface(f, I(id), uv, UV_A, UV_B, UV_C);
            Eigen::MatrixXd L;
            igl::barycentric_coordinates(P, UV_A, UV_B, UV_C, L);

            inMesh.push_back(true);
            
            // Get 3D points for interpolation
            get_triface(f, I(id), v, A, B, C);
            // Update pattern vertex position through barycentric interpolation
            pattern_v.row(id) = A.row(0) * L(0, 0) + B.row(0) * L(0, 1) + C.row(0) * L(0, 2);
        }
        else{
            inMesh.push_back(false);
        }
    }

    // Filter out faces with vertices outside the target mesh

    // Convert pattern faces to std::vector<std::vector<int>> format for processing
    std::vector<std::vector<int>> pattern_polygonal_faces;
    for (int i = 0; i < pattern_f.size(); i++) {
        std::vector<int> face;
        // Handle any number of vertices per face, assuming -1 indicates end of face in some formats
        for (int j = 0; j < pattern_f[i].size(); j++) {
            int vertex_idx = pattern_f[i][j];
            // Some formats use -1 to mark end of face
            if (vertex_idx == -1) break;
            face.push_back(vertex_idx);
        }
        
        // Only add faces with at least 3 vertices
        if (face.size() >= 3) {
            pattern_polygonal_faces.push_back(face);
        }
    }

    for(std::vector<std::vector<int>>::iterator it = pattern_polygonal_faces.begin(); it != pattern_polygonal_faces.end();)
    {
        bool all_in_refMesh = true;
        // iterate vertices
        for(int jd = 0; jd < (*it).size(); jd++)
        {
            int vid = (*it)[jd];
            if(inMesh[vid] == false){
                all_in_refMesh = false;
                break;
            }
        }
        // After checking all vertices of the face, if all_in_refMesh is false (meaning at least one vertex is outside):
        if(!all_in_refMesh){
            it = pattern_polygonal_faces.erase(it);
        }
        else{
            it++;
        }
    }


    return pattern_polygonal_faces;
}

void rescale(Eigen::MatrixXd &V_uv)
{
    // Find min and max values for normalization
    Eigen::Vector2d min_coeff = V_uv.colwise().minCoeff();
    Eigen::Vector2d max_coeff = V_uv.colwise().maxCoeff();
    
    // Compute the size of the bounding box
    Eigen::Vector2d size = max_coeff - min_coeff;
    
    // Translate UV coordinates so minimum is at the origin
    V_uv.col(0) = V_uv.col(0).array() - min_coeff(0);
    V_uv.col(1) = V_uv.col(1).array() - min_coeff(1);
    
    // Scale to fit in a 0-1 box while maintaining aspect ratio
    double scale_factor = 1.0 / std::max(size(0), size(1));
    V_uv *= scale_factor;
}

std::vector<std::vector<int>> map_mesh_with_automatic_parameterization(
    Eigen::Ref<const compas::RowMatrixXd> target_v, 
    Eigen::Ref<const compas::RowMatrixXi> target_f, 
    Eigen::Ref<compas::RowMatrixXd> pattern_v, 
    const std::vector<std::vector<int>>& pattern_f)
{
    // Compute target mesh UV parameterization using LSCM
    Eigen::MatrixXd target_uv;
    
    // Find the open boundary
    Eigen::VectorXi B;
    igl::boundary_loop(target_f, B);

    // Fix two points on the boundary
    Eigen::VectorXi fixed(2, 1);
    fixed(0) = B(0);
    fixed(1) = B(B.size() / 2);

    Eigen::MatrixXd fixed_uv(2, 2);
    fixed_uv << 0, 0, 1, 0;

    // LSCM parametrization
    igl::lscm(target_v, target_f, fixed, fixed_uv, target_uv);
    
    rescale(target_uv);
    

    Eigen::MatrixXd pattern_uv;
    pattern_uv.setZero();
    pattern_uv = pattern_v.leftCols(2);
    
    // rescale(pattern_uv);
    
    // Now perform the mapping using the computed UV parameterizations
    return map_mesh(target_v, target_f, target_uv, pattern_v, pattern_f, pattern_uv);
}

NB_MODULE(_mapping, m)
{
        
    m.def(
        "map_mesh_with_automatic_parameterization",
        &map_mesh_with_automatic_parameterization,
        "Map a 2D pattern mesh onto a 3D target mesh with automatic parameterization.",
        "target_v"_a,
        "target_f"_a,
        "pattern_v"_a,
        "pattern_f"_a);
}