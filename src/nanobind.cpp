#include <nanobind/nanobind.h>
#include "compas.hpp"

NB_MODULE(_nanobind, m) {
    m.doc() = "COMPAS libigl nanobind bindings for geometry processing.";

    m.def("add", [](int a, int b) { return a + b; }, "a"_a, "b"_a,
          "Add two numbers\n\n"
          "Args:\n"
          "    a: First number\n"
          "    b: Second number\n\n"
          "Returns:\n"
          "    Sum of a and b");
}
