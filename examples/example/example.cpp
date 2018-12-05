// build with
// g++ -O3 -Wall -shared -std=c++11 -fPIC -undefined dynamic_lookup example.cpp -o example.so
// includes
// CPLUS_INCLUDE_PATH=/opt/libigl/include:/Users/vanmelet/anaconda3/include/python3.6m:/Users/vanmelet/anaconda3/include/eigen3::/Users/vanmelet/anaconda3/include/python3.6m/pybind11

#include <pybind11/pybind11.h>

int add(int i, int j) {
    return i + j;
}

PYBIND11_MODULE(example, m) {
    m.doc() = "pybind11 example plugin"; // optional module docstring

    m.def("add", &add, "A function which adds two numbers");
}
