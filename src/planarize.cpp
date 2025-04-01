#include "planarize.hpp"

void function(const compas::RowMatrixXd& V, const compas::RowMatrixXi& F) {}

NB_MODULE(_planarize, m) {

    m.def(
        "function_name",
        &function,
        "Description.",
        "V"_a,
        "F"_a);
}