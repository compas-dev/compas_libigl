#include "meshing.hpp"
#include <igl/facet_components.h>

std::tuple<
    compas::RowMatrixXd,
    compas::RowMatrixXi,
    Eigen::VectorXi>
trimesh_remesh_along_isoline(
    compas::RowMatrixXd V1,
    compas::RowMatrixXi F1,
    Eigen::VectorXd S1,
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
    std::tuple<
        compas::RowMatrixXd,
        compas::RowMatrixXi,
        Eigen::VectorXi> result = std::make_tuple(V2, F2, L);

    return result;
}

std::tuple<
    compas::RowMatrixXd,
    compas::RowMatrixXi,
    Eigen::VectorXd>
trimesh_remesh_along_isolines(
    compas::RowMatrixXd V_initial,
    compas::RowMatrixXi F_initial,
    Eigen::VectorXd S_initial,
    Eigen::VectorXd values)
{
    // Initialize with input mesh
    compas::RowMatrixXd V = V_initial;
    compas::RowMatrixXi F = F_initial;
    Eigen::VectorXd S = S_initial;
    
    // Temporary variables for intermediate results
    compas::RowMatrixXd V_temp;
    compas::RowMatrixXi F_temp;
    Eigen::VectorXd S_temp;
    Eigen::VectorXi J;
    Eigen::SparseMatrix<double> BC;
    Eigen::VectorXi L;
    
    // Process each isoline value in sequence
    for (int i = 0; i < values.size(); i++) {
        double val = values(i);
        
        // Remesh along current isoline
        igl::remesh_along_isoline(V, F, S, val, V_temp, F_temp, S_temp, J, BC, L);
        
        // Update mesh for next iteration
        V = V_temp;
        F = F_temp;
        S = S_temp;
    }

    // Return final remeshed geometry and scalar field
    std::tuple<
        compas::RowMatrixXd,
        compas::RowMatrixXi,
        Eigen::VectorXd> result = std::make_tuple(V, F, S);
    
    return result;
}

NB_MODULE(_meshing, m) {
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
        "Remesh a triangle mesh along multiple isolines in sequence.",
        "V"_a,
        "F"_a,
        "S"_a,
        "values"_a);
}
