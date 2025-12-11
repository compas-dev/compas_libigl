#include "cotmatrix.hpp"

Eigen::SparseMatrix<double>
trimesh_cotmatrix(
    Eigen::Ref<const compas::RowMatrixXd> V,
    Eigen::Ref<const compas::RowMatrixXi> F
) {
    Eigen::SparseMatrix<double> L;
    igl::cotmatrix(V, F, L);
    return L;
}

compas::RowMatrixXd
trimesh_cotmatrix_entries(
    Eigen::Ref<const compas::RowMatrixXd> V,
    Eigen::Ref<const compas::RowMatrixXi> F
) {
    Eigen::MatrixXd C;
    igl::cotmatrix_entries(V, F, C);
    compas::RowMatrixXd C_row = C;
    return C_row;
}

NB_MODULE(_cotmatrix, m) {

    m.def(
        "trimesh_cotmatrix",
        &trimesh_cotmatrix,
        "Compute the cotangent Laplacian matrix for a triangle mesh.",
        "V"_a, "F"_a
    );

    m.def(
        "trimesh_cotmatrix_entries",
        &trimesh_cotmatrix_entries,
        "Compute cotangent values for each edge in each triangle.",
        "V"_a, "F"_a
    );
}
