#include <igl/planarize_quad_mesh.h>
#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>

using RowMatrixXd = Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;
using RowMatrixXi = Eigen::Matrix<int, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;


RowMatrixXd planarize(RowMatrixXd V, RowMatrixXi F)
{
    RowMatrixXd Vplanar;

    igl::planarize_quad_mesh(V, F, 100, 0.005, Vplanar);

    return Vplanar;
}

using namespace pybind11::literals;

PYBIND11_MODULE(planarize, m) {
    m.def("planarize", &planarize, "V"_a.noconvert(), "F"_a.noconvert());
}