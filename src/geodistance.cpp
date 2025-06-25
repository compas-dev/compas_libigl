#include "geodistance.hpp"

// Main entry points
compas::VectorXd trimesh_geodistance(
    Eigen::Ref<const compas::RowMatrixXd> V,
    Eigen::Ref<const compas::RowMatrixXi> F,
    int source,
    const std::string& method
) {
    compas::VectorXi sources(1);
    sources << source;

    if (method == "exact") {
        return trimesh_geodistance_exact(V, F, source);
    }
    else if (method == "heat") {
        return trimesh_geodistance_heat(V, F, source);
    }
    throw std::runtime_error("Unknown method: " + method);
}

compas::VectorXd trimesh_geodistance_multiple(
    Eigen::Ref<const compas::RowMatrixXd> V,
    Eigen::Ref<const compas::RowMatrixXi> F,
    Eigen::Ref<const compas::VectorXi> sources,
    const std::string& method
) {
    if (sources.size() == 0) {
        throw std::runtime_error("No source vertices provided");
    }

    if (method == "exact") {
        Eigen::VectorXd D;
        Eigen::VectorXi VS = sources;  // All source vertices
        Eigen::VectorXi FS;  // No face sources
        Eigen::VectorXi VT;  // All vertices as targets
        VT.setLinSpaced(V.rows(), 0, V.rows() - 1);
        Eigen::VectorXi FT;  // No face targets
        igl::exact_geodesic(V, F, VS, FS, VT, FT, D);
        return D;
    }
    else if (method == "heat") {
        igl::HeatGeodesicsData<double> data;
        double t = std::pow(igl::avg_edge_length(V, F), 2);
        igl::heat_geodesics_precompute(V, F, t, data);

        Eigen::VectorXd D = Eigen::VectorXd::Zero(data.Grad.cols());
        // Set all source vertices to 1
        for (int i = 0; i < sources.size(); i++) {
            D(sources(i)) = 1;
        }

        igl::heat_geodesics_solve(data, sources, D);
        return D;
    }
    throw std::runtime_error("Unknown method: " + method);
}

// Implementation details
compas::VectorXd trimesh_geodistance_exact(
    const compas::RowMatrixXd& V,
    const compas::RowMatrixXi& F,
    int vid)
{
    compas::VectorXd D;
    compas::VectorXi VS, FS, VT, FT;

    VS.resize(1);
    VS << vid;

    VT.setLinSpaced(V.rows(), 0, V.rows() - 1);

    igl::exact_geodesic(V, F, VS, FS, VT, FT, D);

    return D;
}

compas::VectorXd trimesh_geodistance_heat(
    const compas::RowMatrixXd& V,
    const compas::RowMatrixXi& F,
    int vid)
{
    compas::VectorXi gamma;
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
        "trimesh_geodistance",
        &trimesh_geodistance,
        "Compute geodesic distances from a source vertex to all other vertices.",
        "V"_a, "F"_a, "source"_a, "method"_a="heat"
    );

    m.def(
        "trimesh_geodistance_multiple",
        &trimesh_geodistance_multiple,
        "Compute geodesic distances from multiple source vertices to all other vertices.",
        "V"_a, "F"_a, "sources"_a, "method"_a="heat"
    );

    m.def(
        "trimesh_geodistance_exact",
        &trimesh_geodistance_exact,
        "Compute exact geodesic distances from a source vertex.",
        "V"_a,
        "F"_a,
        "vid"_a);

    m.def(
        "trimesh_geodistance_heat",
        &trimesh_geodistance_heat,
        "Compute heat method geodesic distances from a source vertex.",
        "V"_a,
        "F"_a,
        "vid"_a);
}