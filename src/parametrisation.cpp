#include "parametrisation.hpp"

void function(const Eigen::MatrixXd& V, const Eigen::MatrixXi& F) {}

NB_MODULE(parametrisation, m) {

    m.def(
        "function_name",
        &function,
        "Description.",
        "V"_a,
        "F"_a);
}