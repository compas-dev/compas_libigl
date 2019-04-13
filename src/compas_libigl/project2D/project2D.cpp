#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <iostream>
using std::vector;
void loadMesh(vector<vector<double>> &vertices, vector<vector<int>> &faces)
{
    for(vector<double> &vlist : vertices){
        vlist[2] = 0;
    }
}

using namespace pybind11::literals;

PYBIND11_MODULE(project2D, m) {
    m.def("loadMesh", [](vector<vector<double>> &vertices, vector<vector<int>> &faces){
        loadMesh(vertices, faces);
        return;
    });
}
