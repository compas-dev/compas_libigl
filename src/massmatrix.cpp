#include "massmatrix.hpp"

Eigen::VectorXd trimesh_massmatrix(compas::RowMatrixXd V, compas::RowMatrixXi F) {
  Eigen::SparseMatrix<double> M;
  igl::massmatrix(V, F, igl::MASSMATRIX_TYPE_VORONOI, M);

  Eigen::VectorXd mass = M.diagonal();

  return mass;
}

NB_MODULE(_massmatrix, m) {

    m.def(
        "trimesh_massmatrix",
        &trimesh_massmatrix,
        "Compute the mass matrix of a triangle mesh.",
        "V"_a,
        "F"_a);
}