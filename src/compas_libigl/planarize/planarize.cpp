#include <igl/planarize_quad_mesh.h>
#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>

using RowMatrixXd = Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;
using RowMatrixXi = Eigen::Matrix<int, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;

namespace py = pybind11;


RowMatrixXd
planarize_quads(
    RowMatrixXd V,
    RowMatrixXi F,
    int maxiter = 100,
    double threshold = 0.005)
{
    RowMatrixXd Vplanar;

    igl::planarize_quad_mesh(V, F, maxiter, threshold, Vplanar);

    return Vplanar;
}


PYBIND11_MODULE(compas_libigl_planarize, m) {
    m.def(
        "planarize_quads",
        &planarize_quads,
        py::arg("V").noconvert(),
        py::arg("F").noconvert(),
        py::arg("maxiter") = 100,
        py::arg("threshold") = 0.005);
}
