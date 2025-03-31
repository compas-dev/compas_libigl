#include "massmatrix.hpp"

void function(const Eigen::MatrixXd& V, const Eigen::MatrixXi& F) {}

NB_MODULE(massmatrix, m) {

    m.def(
        "function_name",
        &function,
        "Description.",
        "V"_a,
        "F"_a);
}