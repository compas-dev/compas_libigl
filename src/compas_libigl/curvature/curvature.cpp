#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <igl/gaussian_curvature.h>
#include <igl/principal_curvature.h>

namespace py = pybind11;

using RowMatrixXd = Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;
using RowMatrixXi = Eigen::Matrix<int, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;


Eigen::VectorXd
trimesh_gaussian_curvature(
    RowMatrixXd V,
    RowMatrixXi F)
{
    Eigen::VectorXd C;
	igl::gaussian_curvature(V, F, C);

    return C;
}


std::tuple<
    Eigen::MatrixXd,
    Eigen::MatrixXd,
    Eigen::VectorXd,
    Eigen::VectorXd>
trimesh_principal_curvature(
    RowMatrixXd V,
    RowMatrixXi F)
{
    Eigen::MatrixXd PD1;
    Eigen::MatrixXd PD2;
    Eigen::VectorXd PV1;
    Eigen::VectorXd PV2;

    std::vector<int> bad_vertices;

	igl::principal_curvature(V, F, PD1, PD2, PV1, PV2, bad_vertices);

    std::tuple<
        Eigen::MatrixXd,
        Eigen::MatrixXd,
        Eigen::VectorXd,
        Eigen::VectorXd> result= std::make_tuple(PD1, PD2, PV1, PV2);

    return result;
}


PYBIND11_MODULE(compas_libigl_curvature, m) {
    m.def(
        "trimesh_gaussian_curvature",
        &trimesh_gaussian_curvature,
        py::arg("V").noconvert(),
        py::arg("F").noconvert()
    );

    m.def(
        "trimesh_principal_curvature",
        &trimesh_principal_curvature,
        py::arg("V").noconvert(),
        py::arg("F").noconvert()
    );
}
