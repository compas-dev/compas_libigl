#include "planarize.hpp"
#include <igl/planarize_quad_mesh.h>

compas::RowMatrixXd
planarize_quads(
    compas::RowMatrixXd V,
    compas::RowMatrixXi F,
    int maxiter,
    double threshold)
{
    compas::RowMatrixXd Vplanar;

    igl::planarize_quad_mesh(V, F, maxiter, threshold, Vplanar);

    return Vplanar;
}

NB_MODULE(_planarize, m) {
    m.def(
        "planarize_quads",
        &planarize_quads,
        "Planarize a quad mesh.",
        "V"_a,
        "F"_a,
        "maxiter"_a,
        "threshold"_a);
}