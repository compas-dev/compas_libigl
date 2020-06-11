#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>
#include <Eigen/StdVector>
#include <igl/boundary_loop.h>

namespace py = pybind11;

using RowMatrixXd = Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;
using RowMatrixXi = Eigen::Matrix<int, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;


std::vector<std::vector<int>>
trimesh_boundaries(
    RowMatrixXd V,
    RowMatrixXi F)
{
    std::vector<std::vector<int>> L;

	igl::boundary_loop(F, L);

    return L;
}


PYBIND11_MODULE(compas_libigl_boundaries, m) {
    m.def(
        "trimesh_boundaries",
        &trimesh_boundaries,
        py::arg("V").noconvert(),
        py::arg("F").noconvert()
    );
}
