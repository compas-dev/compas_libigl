#include "massmatrix.hpp"

Eigen::SparseMatrix<double>
trimesh_massmatrix(
    Eigen::Ref<const compas::RowMatrixXd> V,
    Eigen::Ref<const compas::RowMatrixXi> F,
    const std::string& type
) {
    Eigen::SparseMatrix<double> M;
    igl::massmatrix(V, F, igl::MASSMATRIX_TYPE_BARYCENTRIC, M);
    return M;
}

NB_MODULE(_massmatrix, m) {

    m.def(
        "trimesh_massmatrix",
        &trimesh_massmatrix,
        "Compute the mass matrix for a triangle mesh.",
        "V"_a, "F"_a, "type"_a="barycentric"
    );
}