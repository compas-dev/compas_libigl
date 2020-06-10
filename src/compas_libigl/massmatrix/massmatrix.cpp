#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <igl/massmatrix.h>

namespace py = pybind11;

using RowMatrixXd = Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;
using RowMatrixXi = Eigen::Matrix<int, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;


Eigen::VectorXd
trimesh_massmatrix(
    RowMatrixXd V,
    RowMatrixXi F)
{
    Eigen::SparseMatrix<double> M;
	igl::massmatrix(V, F, igl::MASSMATRIX_TYPE_VORONOI, M);

    // std::cout << M << std::endl;

    Eigen::VectorXd mass = M.diagonal();

    return mass;
}


PYBIND11_MODULE(compas_libigl_massmatrix, m) {
    m.def(
        "trimesh_massmatrix",
        &trimesh_massmatrix,
        py::arg("V").noconvert(),
        py::arg("F").noconvert()
    );
}
