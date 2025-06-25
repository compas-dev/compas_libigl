#include "boundaries.hpp"

compas::VectorVectorInt trimesh_boundaries( Eigen::Ref<const compas::RowMatrixXi> F) {
    compas::VectorVectorInt L;
    igl::boundary_loop(F, L);
    return L;
}

NB_MODULE(_boundaries, m) {
    m.def(
        "trimesh_boundaries",
        &trimesh_boundaries,
        "Compute list of ordered boundary loops for a manifold mesh.",
        "F"_a);
}