#include <vector>
#include <iostream>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "iglMesh.h"

namespace py = pybind11;
using namespace pybind11::literals;


PYBIND11_MODULE(MeshPattern, m)
{
    py::class_<iglMesh>(m, "iglMesh")
            .def(py::init())
            .def("loadMesh", &iglMesh::loadMesh)
            .def("make_flat", &iglMesh::make_flat)
            .def("getVertices",  &iglMesh::getVertices)
            .def("getFaces",  &iglMesh::getFaces);

}
