#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>
#include <Eigen/StdVector>
#include <igl/remesh_along_isoline.h>

namespace py = pybind11;

using RowMatrixXd = Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;
using RowMatrixXi = Eigen::Matrix<int, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;


std::tuple<
    RowMatrixXd,
    RowMatrixXi,
    Eigen::VectorXi>
trimesh_remesh_along_isoline(
    RowMatrixXd V1,
    RowMatrixXi F1,
    Eigen::VectorXd S1,
    double s)
{
    RowMatrixXd V2;
    RowMatrixXi F2;
    Eigen::VectorXd S2;

    Eigen::VectorXi J;
    Eigen::SparseMatrix<double> BC;
    Eigen::VectorXi L;

	igl::remesh_along_isoline(V1, F1, S1, s, V2, F2, S2, J, BC, L);

    std::tuple<
        RowMatrixXd,
        RowMatrixXi,
        Eigen::VectorXi> result = std::make_tuple(V2, F2, L);

    return result;
}


PYBIND11_MODULE(compas_libigl_meshing, m) {
    m.def(
        "trimesh_remesh_along_isoline",
        &trimesh_remesh_along_isoline,
        py::arg("V1").noconvert(),
        py::arg("F1").noconvert(),
        py::arg("S1"),
        py::arg("s")
    );
}
