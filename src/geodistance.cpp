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

// Multiple source points - exact method
Eigen::VectorXd
trimesh_geodistance_exact_multiple(
    const compas::RowMatrixXd& V,
    const compas::RowMatrixXi& F,
    const Eigen::VectorXi& source_vertices)
{
    Eigen::VectorXi VS, FS, VT, FT;
    Eigen::VectorXd D;

    // Set source vertices
    VS = source_vertices;

    // Set target vertices to all vertices
    VT.setLinSpaced(V.rows(), 0, V.rows() - 1);

    // Empty source faces and target faces
    FS.resize(0);
    FT.resize(0);

    igl::exact_geodesic(V, F, VS, FS, VT, FT, D);

    return D;
}

// Multiple source points - heat method
Eigen::VectorXd
trimesh_geodistance_heat_multiple(
    const compas::RowMatrixXd& V,
    const compas::RowMatrixXi& F,
    const Eigen::VectorXi& source_vertices)
{
    igl::HeatGeodesicsData<double> data;
    double t = std::pow(igl::avg_edge_length(V, F), 2);
    igl::heat_geodesics_precompute(V, F, t, data);

    // Initialize distance vector
    Eigen::VectorXd D = Eigen::VectorXd::Zero(data.Grad.cols());
    
    // Set source vertices
    for(int i = 0; i < source_vertices.size(); i++) {
        D(source_vertices(i)) = 1;
    }

    igl::heat_geodesics_solve(data, source_vertices, D);

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

    m.def(
        "trimesh_geodistance_exact_multiple",
        &trimesh_geodistance_exact_multiple,
        "Description.",
        "V"_a,
        "F"_a,
        "source_vertices"_a);

    m.def(
        "trimesh_geodistance_heat_multiple",
        &trimesh_geodistance_heat_multiple,
        "Description.",
        "V"_a,
        "F"_a,
        "source_vertices"_a);
}