#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <igl/boundary_loop.h>
#include <igl/map_vertices_to_circle.h>
#include <igl/harmonic.h>
#include <igl/lscm.h>

namespace py = pybind11;

using RowMatrixXd = Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;
using RowMatrixXi = Eigen::Matrix<int, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;


Eigen::MatrixXd
trimesh_harmonic_map(
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


Eigen::MatrixXd
trimesh_lscm(
    RowMatrixXd V,
    RowMatrixXi F)
{
    Eigen::MatrixXd V_uv;

    // Find the open boundary
    Eigen::VectorXi B;
    igl::boundary_loop(F, B);

    // Fix two points on the boundary
    Eigen::VectorXi fixed(2, 1);
    fixed(0) = B(0);
    fixed(1) = B(B.size() / 2);

    Eigen::MatrixXd fixed_uv(2, 2);
    fixed_uv << 0, 0, 1, 0;

    // LSCM parametrization
    igl::lscm(V, F, fixed, fixed_uv, V_uv);

    return V_uv;
}


PYBIND11_MODULE(compas_libigl_parametrisation, m) {
    m.def(
        "trimesh_harmonic_map",
        &trimesh_harmonic_map,
        py::arg("V").noconvert(),
        py::arg("F").noconvert()
    );

    m.def(
        "trimesh_lscm",
        &trimesh_lscm,
        py::arg("V").noconvert(),
        py::arg("F").noconvert()
    );
}
