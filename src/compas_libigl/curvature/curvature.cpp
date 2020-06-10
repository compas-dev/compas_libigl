#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <igl/gaussian_curvature.h>

namespace py = pybind11;

using RowMatrixXd = Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;
using RowMatrixXi = Eigen::Matrix<int, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;


Eigen::VectorXd
trimesh_curvature(
    RowMatrixXd V,
    RowMatrixXi F)
{
    Eigen::VectorXd C;
	igl::gaussian_curvature(V, F, C);

    return C;
}


PYBIND11_MODULE(compas_libigl_curvature, m) {
    m.def(
        "trimesh_curvature",
        &trimesh_curvature,
        py::arg("V").noconvert(),
        py::arg("F").noconvert()
    );
}
