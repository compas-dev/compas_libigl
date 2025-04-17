#include "mapping.hpp"



void cleanMesh(
    const compas::RowMatrixXd& V_in, 
    const compas::RowMatrixXi& F_in, 
    std::vector<std::vector<int>>& faces_)
{
    // Make local copies of input matrices that we can modify
    compas::RowMatrixXd V_ = V_in;
    compas::RowMatrixXi F_ = F_in;
    
    // Convert std::vector<std::vector<int>> to the format expected by polygons_to_triangles
    Eigen::VectorXi I;    // Vectorized list of polygon corner indices
    Eigen::VectorXi C;    // Cumulative polygon sizes
    compas::RowMatrixXi F;    // Triangle faces (output)
    Eigen::VectorXi J;    // Index map (output)
    
    // Calculate total number of indices across all polygons
    int total_indices = 0;
    for (const auto& face : faces_) {
        total_indices += face.size();
    }
    
    // Initialize I with all indices and C with cumulative counts
    I.resize(total_indices);
    C.resize(faces_.size() + 1);
    
    int idx = 0;
    C(0) = 0;
    for (int i = 0; i < faces_.size(); i++) {
        for (int j = 0; j < faces_[i].size(); j++) {
            I(idx++) = faces_[i][j];
        }
        C(i+1) = C(i) + faces_[i].size();
    }
    
    // Convert polygons to triangles
    igl::polygons_to_triangles(I, C, F_, J);

    //remove duplicate
    compas::RowMatrixXd SV;
    compas::RowMatrixXi SF;
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


    std::vector<bool> inList; inList.resize(V_.rows(), false);
    for(int id = 0; id < faces_.size(); id++)
    {
        for(int jd = 0; jd < faces_[id].size(); jd++)
        {
            inList[faces_[id][jd]] = true;
        }
    }

    int count = 0;
    std::vector<int> newIndex;
    for(int id = 0; id < inList.size(); id++){
        if(inList[id]) {
            newIndex.push_back(count++);
        }
        else{
            newIndex.push_back(-1);
        }
    }

    SV = compas::RowMatrixXd(count, 3);
    for(int id = 0; id < inList.size(); id++){
        if(inList[id]){
            SV.row(newIndex[id]) = V_.row(id);
        }
    }

    for(int id = 0; id < faces_.size(); id++)
    {
        for(int jd = 0; jd < faces_[id].size(); jd++)
        {
            faces_[id][jd] = newIndex[faces_[id][jd]];
        }
    }
    V_ = SV;

    // Convert std::vector<std::vector<int>> to the format expected by polygons_to_triangles again
    // Recalculate because faces_ has been updated
    total_indices = 0;
    for (const auto& face : faces_) {
        total_indices += face.size();
    }
    
    I.resize(total_indices);
    C.resize(faces_.size() + 1);
    
    idx = 0;
    C(0) = 0;
    for (int i = 0; i < faces_.size(); i++) {
        for (int j = 0; j < faces_[i].size(); j++) {
            I(idx++) = faces_[i][j];
        }
        C(i+1) = C(i) + faces_[i].size();
    }
    
    // Convert polygons to triangles
    igl::polygons_to_triangles(I, C, F_, J);
    
    return;
}

void getTriFace(
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

bool mapPoint3D_simple(
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
            getTriFace(F_, id, UV_, A, B, C);
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

void iglMesh::mapMesh3D_simple(iglMesh &baseMesh)
{
    // Sets UV matrix for xy coordinates
    // if(UV_.isZero()){
    //     parametrization_simple();
    // }

    std::vector<bool> inMesh;
    int count = 0;
    for(int id = 0; id < baseMesh.V_.rows(); id++)
    {
        Eigen::Vector3d pt = baseMesh.V_.row(id);
        Eigen::Vector3d l(0, 0, 0);
        int faceID = -1;
        if(mapPoint3D_simple(F_, UV_, pt, l, faceID))
        {
            compas::RowMatrixXd A, B, C;
            getTriFace(F_, faceID, V_, A, B, C);
            baseMesh.V_.row(id) = A.row(0) * l(0) + B.row(0) * l(1) + C.row(0) * l(2);
            inMesh.push_back(true);
        }
        else{
            inMesh.push_back(false);
        }
    }

    for(std::vector<std::vector<int>>::iterator it = baseMesh.faces_.begin(); it != baseMesh.faces_.end();)
    {
        bool all_in_refMesh = true;
        for(int jd = 0; jd < (*it).size(); jd++)
        {
            int vid = (*it)[jd];
            if(inMesh[vid] == false){
                all_in_refMesh = false;
                break;
            }
        }
        if(!all_in_refMesh)
        {
            it = baseMesh.faces_.erase(it);
        }
        else{
            it++;
        }
    }

    cleanMesh(baseMesh.V_, baseMesh.F_, baseMesh.faces_);
}

void mapMesh3D_AABB(
    Eigen::Ref<const compas::RowMatrixXd>v, 
    Eigen::Ref<const compas::RowMatrixXi>f, 
    Eigen::Ref<const compas::RowMatrixXd> uv,
    Eigen::Ref<compas::RowMatrixXd>  pattern_v, 
    Eigen::Ref<const compas::RowMatrixXi> pattern_f, 
    Eigen::Ref<const compas::RowMatrixXd> pattern_uv, 
    std::vector<std::vector<int>>& pattern_polygonal_faces)
{


    std::cout << "Mapping 2D pattern mesh onto 3D target mesh" << std::endl;
    for (int id = 0; id < pattern_v.rows(); id++)
    {
        std::cout << pattern_v.row(id) << std::endl;
    }
    // Sets UV matrix for xy coordinates
    // if(UV_.isZero()){
    //     parametrization_lscm();
    // }

    // Use regular MatrixXd to avoid type conflicts with AABB functions
    Eigen::MatrixXd V_uv = uv;
    Eigen::MatrixXi F_faces = f;
    
    igl::AABB<Eigen::MatrixXd, 2> tree;
    tree.init(V_uv, F_faces);

    std::vector<bool> inMesh;
    // Pattern must have parametrization
    // baseMesh.parametrization_simple();
    Eigen::MatrixXd C;
    Eigen::VectorXi I;
    Eigen::VectorXd sqrD;
    Eigen::MatrixXd pattern_uv_eigen = pattern_uv;
    
    tree.squared_distance(V_uv, F_faces, pattern_uv_eigen, sqrD, I, C);
    
    for(int id = 0; id < pattern_uv.rows(); id++)
    {
        if(std::fabs(sqrD[id]) < 1e-5)
        {
            compas::RowMatrixXd A, B, C;
            Eigen::MatrixXd P(1, 3);
            P << pattern_uv(id, 0), pattern_uv(id, 1), 0;
            compas::RowMatrixXd UV_A, UV_B, UV_C;
            getTriFace(f, I(id), uv, UV_A, UV_B, UV_C);
            Eigen::MatrixXd L;
            igl::barycentric_coordinates(P, UV_A, UV_B, UV_C, L);

            inMesh.push_back(true);
            
            // Get 3D points for interpolation
            getTriFace(f, I(id), v, A, B, C);
            // Update pattern vertex position through barycentric interpolation
            pattern_v.row(id) = A.row(0) * L(0, 0) + B.row(0) * L(0, 1) + C.row(0) * L(0, 2);
        }
        else{
            inMesh.push_back(false);
        }
    }

    for(std::vector<std::vector<int>>::iterator it = pattern_polygonal_faces.begin(); it != pattern_polygonal_faces.end();)
    {
        bool all_in_refMesh = true;
        for(int jd = 0; jd < (*it).size(); jd++)
        {
            int vid = (*it)[jd];
            if(inMesh[vid] == false){
                all_in_refMesh = false;
                break;
            }
        }
        if(!all_in_refMesh){
            it = pattern_polygonal_faces.erase(it);
        }
        else{
            it++;
        }
    }
    std::cout << "Mapping 2D pattern mesh onto 3D target mesh" << std::endl;
    for (int id = 0; id < pattern_v.rows(); id++)
    {
        std::cout << pattern_v.row(id) << std::endl;
    }
    cleanMesh(pattern_v, pattern_f, pattern_polygonal_faces);
}


// Create the nanobind module
NB_MODULE(_mapping, m) {
    m.def(
        "mapMesh3D_AABB",
        &mapMesh3D_AABB,
        "Map a 2D pattern mesh onto a 3D target mesh using simple UV parameterization",
        "v"_a,
        "f"_a,
        "uv"_a,
        "pattern_v"_a,
        "pattern_f"_a,
        "pattern_uv"_a,
        "pattern_polygonal_faces"_a
        );
}