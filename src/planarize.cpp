#include "planarize.hpp"


compas::RowMatrixXd planarize_quads(compas::RowMatrixXd V, compas::RowMatrixXi F, int maxiter = 100, double threshold = 0.005) {
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