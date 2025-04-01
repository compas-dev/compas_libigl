#include "isolines.hpp"

std::tuple<compas::RowMatrixXd, compas::RowMatrixXi, compas::RowMatrixXi> trimesh_isolines(
    const compas::RowMatrixXd V,  // by dim list of mesh vertex positions
    const compas::RowMatrixXi F,  // by 3 list of mesh triangle indices into some V
    const Eigen::VectorXd  isovalues,     // by dim list of vertex positions
    const Eigen::VectorXd vals)   // List of values for isolines
{
  compas::RowMatrixXd iV;  // iV by dim list of isoline vertex positions
  compas::RowMatrixXi iE;  // iE by 2 list of edge indices into iV
  Eigen::VectorXi I;  // ieE by 1 list of indices into vals indicating which value

//   igl::isolines(V, F, V.col(1).eval(), vals, iV, iE, I);
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
        "vals"_a);
}