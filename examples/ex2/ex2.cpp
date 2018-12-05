// g++ -O3 -Wall -shared -std=c++11 -fPIC -undefined dynamic_lookup ex2.cpp -o ex2.so

#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>

#include <iostream>

namespace py = pybind11;

void test_numpy_array(Eigen::MatrixXd M) {

	std::cout << M(0, 1);

}

PYBIND11_MODULE(ex2, m) {

    m.def("test_numpy_array", &test_numpy_array, "test array passing");

}
