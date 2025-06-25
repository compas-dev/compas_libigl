#include "isolines.hpp"

compas::IsolinesResult trimesh_isolines(
    Eigen::Ref<const compas::RowMatrixXd> V,
    Eigen::Ref<const compas::RowMatrixXi> F,
    Eigen::Ref<const Eigen::VectorXd> isovalues,
    Eigen::Ref<const Eigen::VectorXd> vals)
{
    compas::RowMatrixXd iV;  // iV by dim list of isoline vertex positions
    compas::RowMatrixXi iE;  // iE by 2 list of edge indices into iV
    Eigen::VectorXi I;       // ieE by 1 list of indices into vals indicating which value

    igl::isolines(V, F, isovalues, vals, iV, iE, I);

    return std::make_tuple(iV, iE, I);
}

NB_MODULE(_isolines, m) {
    
    m.doc() = "Isoline computation functions using libigl";

    m.def(
        "trimesh_isolines",
        &trimesh_isolines,
        "Compute the isolines of a triangle mesh.",
        "V"_a,
        "F"_a,
        "isovalues"_a,
        "vals"_a
    );
}