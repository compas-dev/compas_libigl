#include "meshing.hpp"

compas::RemeshIsolineResult
trimesh_remesh_along_isoline(
    Eigen::Ref<const compas::RowMatrixXd> V1,
    Eigen::Ref<const compas::RowMatrixXi> F1,
    Eigen::Ref<const Eigen::VectorXd> S1,
    double s)
{
    // Check initial face components
    Eigen::VectorXi C1;
    igl::facet_components(F1, C1);
    const int fc_count_before = C1.maxCoeff() + 1;  // +1 because maxCoeff gives max index

    // Output variables for remeshing
    compas::RowMatrixXd V2;
    compas::RowMatrixXi F2;
    Eigen::VectorXd S2;
    Eigen::VectorXi J;
    Eigen::SparseMatrix<double> BC;
    Eigen::VectorXi L;

    // Remesh along isoline
    igl::remesh_along_isoline(V1, F1, S1, s, V2, F2, S2, J, BC, L);

    // Check face components after remeshing
    Eigen::VectorXi C2;
    igl::facet_components(F2, C2);
    const int fc_count_after = C2.maxCoeff() + 1;

    // If component count changed, something went wrong
    if (fc_count_before != fc_count_after) {
        throw std::runtime_error("Face component count changed after remeshing");
    }

    // Return remeshed geometry and labels
    return std::make_tuple(V2, F2, L);
}

compas::RemeshIsolinesResult
trimesh_remesh_along_isolines(
    Eigen::Ref<const compas::RowMatrixXd> V_initial,
    Eigen::Ref<const compas::RowMatrixXi> F_initial,
    Eigen::Ref<const Eigen::VectorXd> S_initial,
    Eigen::Ref<const Eigen::VectorXd> values)
{
    // Pre-allocate all matrices with initial size
    compas::RowMatrixXd V = V_initial;
    compas::RowMatrixXi F = F_initial;
    Eigen::VectorXd S = S_initial;
    
    // Initialize face groups
    Eigen::VectorXi face_groups = Eigen::VectorXi::Zero(F.rows());
    
    // Temporary variables - pre-allocated once
    compas::RowMatrixXd V_temp;
    compas::RowMatrixXi F_temp;
    Eigen::VectorXd S_temp;
    Eigen::VectorXi J, L;
    Eigen::SparseMatrix<double> BC;
    
    // Process each isoline value in sequence
    for (int i = 0; i < values.size(); i++) {
        // Remesh along current isoline
        igl::remesh_along_isoline(V, F, S, values[i], V_temp, F_temp, S_temp, J, BC, L);
        
        // Update face groups - pre-allocate new array
        Eigen::VectorXi new_face_groups = Eigen::VectorXi::Zero(F_temp.rows());
        
        // Update face groups efficiently
        for(Eigen::Index f = 0; f < F_temp.rows(); f++) {
            if(J[f] >= 0) {
                new_face_groups[f] = face_groups[J[f]];
                if(L[f] == 1) {
                    new_face_groups[f] = i + 1;  // Use iteration number + 1 as group ID
                }
            } else {
                new_face_groups[f] = i + 1;
            }
        }
        
        // Copy instead of move since we're using references
        V = V_temp;
        F = F_temp;
        S = S_temp;
        face_groups = new_face_groups;
    }

    return std::make_tuple(V, F, S, face_groups);
}

NB_MODULE(_meshing, m) {
    m.doc() = "Mesh remeshing functions using libigl";

    m.def(
        "trimesh_remesh_along_isoline",
        &trimesh_remesh_along_isoline,
        "Remesh a triangle mesh along an isoline. Preserves the number of connected components.",
        "V1"_a,
        "F1"_a,
        "S1"_a,
        "s"_a);
        
    m.def(
        "trimesh_remesh_along_isolines",
        &trimesh_remesh_along_isolines,
        "Remesh a triangle mesh along multiple isolines. Returns mesh data and face group IDs.",
        "V1"_a,
        "F1"_a,
        "S1"_a,
        "values"_a);
}
