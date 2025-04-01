#include "geodistance.hpp"

Eigen::VectorXd
trimesh_geodistance_exact(
    const compas::RowMatrixXd& V,
    const compas::RowMatrixXi& F,
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
    const compas::RowMatrixXd& V,
    const compas::RowMatrixXi& F,
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




NB_MODULE(_geodistance, m) {

    m.def(
        "trimesh_geodistance_exact",
        &trimesh_geodistance_exact,
        "Description.",
        "V"_a,
        "F"_a,
        "vid"_a);

    m.def(
        "trimesh_geodistance_heat",
        &trimesh_geodistance_heat,
        "Description.",
        "V"_a,
        "F"_a,
        "vid"_a);
}