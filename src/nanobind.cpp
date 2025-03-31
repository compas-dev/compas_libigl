#include <nanobind/nanobind.h>
#include "compas.h"

NB_MODULE(nanobind, m) {
    m.doc() = "COMPAS libigl nanobindbindings for geometry processing.";

    m.def("add", [](int a, int b) { return a + b; }, "a"_a, "b"_a,
          "Add two numbers\n\n"
          "Args:\n"
          "    a: First number\n"
          "    b: Second number\n\n"
          "Returns:\n"
          "    Sum of a and b");
}
