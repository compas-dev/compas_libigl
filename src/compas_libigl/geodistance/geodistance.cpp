#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <igl/avg_edge_length.h>
#include <igl/exact_geodesic.h>
#include <igl/heat_geodesics.h>

using RowMatrixXd = Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;
using RowMatrixXi = Eigen::Matrix<int, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;

namespace py = pybind11;


Eigen::VectorXd
trimesh_geodistance_exact(
    RowMatrixXd V,
    RowMatrixXi F,
    int vid)
{
	Eigen::VectorXd D;
	Eigen::VectorXi VS, FS, VT, FT;

	VS.resize(1);
	VS << vid;

	VT.setLinSpaced(V.rows(), 0, V.rows() - 1);

	igl::exact_geodesic(V, F, VS, FS, VT, FT, D);

    return D;
}


Eigen::VectorXd
trimesh_geodistance_heat(
    RowMatrixXd V,
    RowMatrixXi F,
    int vid)
{
    Eigen::VectorXi gamma;
    gamma.resize(1);
    gamma << vid;

    igl::HeatGeodesicsData<double> data;
    double t = std::pow(igl::avg_edge_length(V, F), 2);
    igl::heat_geodesics_precompute(V, F, t, data);

    Eigen::VectorXd D = Eigen::VectorXd::Zero(data.Grad.cols());
    D(vid) = 1;

    igl::heat_geodesics_solve(data, gamma, D);

    return D;
}


PYBIND11_MODULE(compas_libigl_geodistance, m) {
    m.def(
        "trimesh_geodistance_exact",
        &trimesh_geodistance_exact,
        py::arg("V").noconvert(),
        py::arg("F").noconvert(),
        py::arg("vid")
    );

    m.def(
        "trimesh_geodistance_heat",
        &trimesh_geodistance_heat,
        py::arg("V").noconvert(),
        py::arg("F").noconvert(),
        py::arg("vid")
    );
}
