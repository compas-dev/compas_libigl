#include "parametrisation.hpp"
#include <igl/boundary_loop.h>
#include <igl/harmonic.h>
#include <igl/lscm.h>
#include <igl/map_vertices_to_circle.h>
#include <Eigen/Core>

void rescale(Eigen::MatrixXd &V_uv)
{
    // Find min and max values for normalization
    Eigen::Vector2d min_coeff = V_uv.colwise().minCoeff();
    Eigen::Vector2d max_coeff = V_uv.colwise().maxCoeff();
    
    // Compute the size of the bounding box
    Eigen::Vector2d size = max_coeff - min_coeff;
    
    // Translate UV coordinates so minimum is at the origin
    V_uv.col(0) = V_uv.col(0).array() - min_coeff(0);
    V_uv.col(1) = V_uv.col(1).array() - min_coeff(1);
    
    // Scale to fit in a 0-1 box while maintaining aspect ratio
    double scale_factor = 1.0 / std::max(size(0), size(1));
    V_uv *= scale_factor;
}

Eigen::MatrixXd
harmonic(
    Eigen::Ref<const compas::RowMatrixXd> V,
    Eigen::Ref<const compas::RowMatrixXi> F)
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

    rescale(V_uv);

    return V_uv;
}

Eigen::MatrixXd
lscm(
    Eigen::Ref<const compas::RowMatrixXd> V,
    Eigen::Ref<const compas::RowMatrixXi> F)
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
    
    rescale(V_uv);

    return V_uv;
}

NB_MODULE(_parametrisation, m) {
    m.def(
        "harmonic",
        &harmonic,
        "Compute the harmonic parametrization of a triangle mesh.",
        "V"_a,
        "F"_a);

    m.def(
        "lscm",
        &lscm,
        "Compute the least-squares conformal map of a triangle mesh.",
        "V"_a,
        "F"_a);

}