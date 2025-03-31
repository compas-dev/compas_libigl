#include "meshing.hpp"

void function(const Eigen::MatrixXd& V, const Eigen::MatrixXi& F) {}

NB_MODULE(meshing, m) {

    m.def(
        "function_name",
        &function,
        "Description.",
        "V"_a,
        "F"_a);
}