#include "simplify.hpp"

std::tuple<compas::RowMatrixXd, Eigen::VectorXi, Eigen::VectorXi>
ramer_douglas_peucker(
    Eigen::Ref<const compas::RowMatrixXd> P,
    double threshold
) {
    Eigen::MatrixXd S;  // Simplified polyline
    Eigen::VectorXi J;  // Indices of kept points in original polyline
    Eigen::VectorXi Q;  // For each point in S, index in original P

    igl::ramer_douglas_peucker(P, threshold, S, J, Q);

    compas::RowMatrixXd S_row = S;
    return std::make_tuple(S_row, J, Q);
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
