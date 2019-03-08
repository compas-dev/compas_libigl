// requires triangle.h
// g++ -O3 -Wall -shared -std=c++11 -fPIC -undefined dynamic_lookup -I/opt/triangle triangulation.cpp -o triangulation.so
// triangle library also needs to be compiled
// tried: cc -O -I/opt/local/include -L/opt/local/lib -shared -o triangle.so triangle.c -lm
// but doesn't change anything

#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <iostream>
#include <igl/triangle/triangulate.h>


using RowMatrixXd = Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;
using RowMatrixXi = Eigen::Matrix<int, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;

namespace py = pybind11;


struct Result {
	RowMatrixXd vertices;
	RowMatrixXi faces;
};


Result polygon(RowMatrixXd V, RowMatrixXi E)
{
	RowMatrixXd H;

	RowMatrixXd V2;
	RowMatrixXi F2;

	igl::triangle::triangulate(V, E, H, "a0.005q", V2, F2);

	Result result;
    
    RowMatrixXd V2_3D = RowMatrixXd::Zero(V2.rows(), V2.cols() + 1);
    V2_3D.leftCols(V2.cols()) = V2;
	
    result.vertices = V2_3D;
	result.faces = F2;

	return result;
}


PYBIND11_MODULE(triangulation, m) {
    m.def("polygon", &polygon, py::arg("V").noconvert(), py::arg("E").noconvert());

    py::class_<Result>(m, "Result")
    	.def_readonly("vertices", &Result::vertices)
    	.def_readonly("faces", &Result::faces);
}
