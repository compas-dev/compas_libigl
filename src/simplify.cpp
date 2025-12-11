#include "simplify.hpp"

std::tuple<compas::RowMatrixXd, Eigen::VectorXi, compas::RowMatrixXd>
ramer_douglas_peucker(
    Eigen::Ref<const compas::RowMatrixXd> P,
    double threshold
) {
    Eigen::MatrixXd S;  // Simplified polyline
    Eigen::VectorXi J;  // Indices of kept points in original polyline
    Eigen::MatrixXd Q;  // For each point in original P, the corresponding point on simplified curve

    igl::ramer_douglas_peucker(P, threshold, S, J, Q);

    compas::RowMatrixXd S_row = S;
    compas::RowMatrixXd Q_row = Q;
    return std::make_tuple(S_row, J, Q_row);
}

NB_MODULE(_simplify, m) {
    m.doc() = "Polyline simplification functions using libigl";

    m.def(
        "ramer_douglas_peucker",
        &ramer_douglas_peucker,
        "Simplify a polyline using Ramer-Douglas-Peucker algorithm.",
        "P"_a,
        "threshold"_a);
}
