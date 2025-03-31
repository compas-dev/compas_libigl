#include <nanobind/nanobind.h>
#include "compas.h"

namespace nb = nanobind;

using namespace nb::literals;

NB_MODULE(_libigl, m) {
    m.doc() = "COMPAS libigl bindings for geometry processing";

    m.def("add", [](int a, int b) { return a + b; }, "a"_a, "b"_a,
          "Add two numbers\n\n"
          "Args:\n"
          "    a: First number\n"
          "    b: Second number\n\n"
          "Returns:\n"
          "    Sum of a and b");
}
