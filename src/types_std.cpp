#include "types_std.hpp"

NB_MODULE(_types_std, m) {

    nb::bind_vector<std::vector<double>>(m, "VectorDouble");
    nb::bind_vector<std::vector<int>>(m, "VectorInt");
    nb::bind_vector<std::vector<bool>>(m, "VectorBool");
    nb::bind_vector<std::vector<std::vector<int>>>(m, "VectorVectorInt");
    nb::bind_vector<std::vector<compas::RowMatrixXd>>(m, "VectorRowMatrixXd");
    nb::bind_vector<std::vector<std::tuple<int, float, float, float>>>(m, "VectorTupleIntFloatFloatFloat");
    nb::bind_vector<std::vector<std::vector<std::tuple<int, float, float, float>>>>(m, "VectorVectorTupleIntFloatFloatFloat");
}