#include "curvature.hpp"

Eigen::VectorXd trimesh_gaussian_curvature(const compas::RowMatrixXd& V, const compas::RowMatrixXi& F) {
    Eigen::VectorXd C;
    igl::gaussian_curvature(V, F, C);
    return C;
}

std::tuple<Eigen::MatrixXd, Eigen::MatrixXd, Eigen::VectorXd, Eigen::VectorXd>
trimesh_principal_curvature(const compas::RowMatrixXd& V, const compas::RowMatrixXi& F) {
    if (F.cols() != 3) {
        std::cerr << "Error: Principal curvature requires triangular faces." << std::endl;
        return std::make_tuple(Eigen::MatrixXd(), Eigen::MatrixXd(),
                             Eigen::VectorXd(), Eigen::VectorXd());
    }

    Eigen::MatrixXd PD1, PD2;
    Eigen::VectorXd PV1, PV2;
    std::vector<int> bad_vertices;

    igl::principal_curvature(V, F, PD1, PD2, PV1, PV2, bad_vertices);

    return std::make_tuple(PD1, PD2, PV1, PV2);
}

NB_MODULE(_curvature, m) {
    m.def(
        "trimesh_gaussian_curvature",
        &trimesh_gaussian_curvature,
        "Compute the discrete gaussian curvature of a triangle mesh.",
        "V"_a, "F"_a
    );

    m.def(
        "trimesh_principal_curvature",
        &trimesh_principal_curvature,
        "Compute the principal curvatures and directions of a triangle mesh.",
        "V"_a, "F"_a
    );
}