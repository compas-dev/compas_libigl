#include "curvature.hpp"


compas::PrincipalCurvatureResult
trimesh_principal_curvature(
    Eigen::Ref<const compas::RowMatrixXd> V,
    Eigen::Ref<const compas::RowMatrixXi> F,
    int radius
) {
    compas::RowMatrixXd PD1, PD2;
    compas::VectorXd PV1, PV2;
    igl::principal_curvature(V, F, PD1, PD2, PV1, PV2, radius);
    return std::make_tuple(PD1, PD2, PV1, PV2);
}

compas::VectorXd
trimesh_gaussian_curvature(
    Eigen::Ref<const compas::RowMatrixXd> V,
    Eigen::Ref<const compas::RowMatrixXi> F
) {
    compas::VectorXd K;
    igl::gaussian_curvature(V, F, K);
    return K;
}

NB_MODULE(_curvature, m) {

    m.doc() = "Mesh curvature computation functions using libigl";

    m.def(
        "trimesh_principal_curvature",
        &trimesh_principal_curvature,
        "Compute principal curvatures of a triangle mesh.",
        "V"_a, "F"_a, "radius"_a=5
    );

    m.def(
        "trimesh_gaussian_curvature",
        &trimesh_gaussian_curvature,
        "Compute Gaussian curvature of a triangle mesh.",
        "V"_a, "F"_a
    );

}