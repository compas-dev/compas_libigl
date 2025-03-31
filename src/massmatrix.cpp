#include "massmatrix.hpp"

void function(const Eigen::MatrixXd& V, const Eigen::MatrixXi& F) {}

NB_MODULE(_massmatrix, m) {

    m.def(
        "function_name",
        &function,
        "Description.",
        "V"_a,
        "F"_a);
}