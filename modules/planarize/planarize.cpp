#include <igl/planarize_quad_mesh.h>
#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>


using RowMatrixXd = Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;
using RowMatrixXi = Eigen::Matrix<int, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;


RowMatrixXd planarize_quads(RowMatrixXd V, RowMatrixXi F, int maxiter = 100, double threshold = 0.005)
{
    RowMatrixXd Vplanar;

    igl::planarize_quad_mesh(V, F, maxiter, threshold, Vplanar);

    return Vplanar;
}

using namespace pybind11::literals;

PYBIND11_MODULE(planarize, m) {
    m.def("planarize_quads",
          &planarize_quads,
          "V"_a.noconvert(),
          "F"_a.noconvert(),
          pybind11::arg("maxiter") = 100,
          pybind11::arg("threshold") = 0.005);
}
