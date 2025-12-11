#include "grad.hpp"

Eigen::SparseMatrix<double>
trimesh_grad(
    Eigen::Ref<const compas::RowMatrixXd> V,
    Eigen::Ref<const compas::RowMatrixXi> F
) {
    Eigen::SparseMatrix<double> G;
    igl::grad(V, F, G);
    return G;
}

NB_MODULE(_grad, m) {

    m.def(
        "trimesh_grad",
        &trimesh_grad,
        "Compute the gradient operator for a triangle mesh.",
        "V"_a, "F"_a
    );
}
