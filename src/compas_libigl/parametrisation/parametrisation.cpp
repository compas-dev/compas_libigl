#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <igl/boundary_loop.h>
#include <igl/map_vertices_to_circle.h>
#include <igl/harmonic.h>

namespace py = pybind11;

using RowMatrixXd = Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;
using RowMatrixXi = Eigen::Matrix<int, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;


Eigen::MatrixXd
trimesh_parametrisation_harmonic(
    RowMatrixXd V,
    RowMatrixXi F)
{
    Eigen::MatrixXd V_uv;

    // Find the open boundary
    Eigen::VectorXi B;
    igl::boundary_loop(F, B);

    // Map the boundary to a circle, preserving edge proportions
    Eigen::MatrixXd B_uv;
    igl::map_vertices_to_circle(V, B, B_uv);

    // Harmonic parametrization for the internal vertices
    igl::harmonic(V, F, B, B_uv, 1, V_uv);

    return V_uv;
}


PYBIND11_MODULE(compas_libigl_parametrisation, m) {
    m.def(
        "trimesh_parametrisation_harmonic",
        &trimesh_parametrisation_harmonic,
        py::arg("V").noconvert(),
        py::arg("F").noconvert()
    );
}
