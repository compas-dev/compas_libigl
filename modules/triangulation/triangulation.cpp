#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <iostream>
#include <igl/triangle/triangulate.h>


using RowMatrixXd = Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;
using RowMatrixXi = Eigen::Matrix<int, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;

namespace py = pybind11;


struct Triangulation {
	RowMatrixXd vertices;
	RowMatrixXi faces;
};


Triangulation triangulate_polygon(RowMatrixXd V, RowMatrixXi E)
{
	RowMatrixXd H;

	RowMatrixXd V2;
	RowMatrixXi F2;

	igl::triangle::triangulate(V, E, H, "a0.005q", V2, F2);

	Triangulation tri;

    RowMatrixXd V2_3D = RowMatrixXd::Zero(V2.rows(), V2.cols() + 1);
    V2_3D.leftCols(V2.cols()) = V2;

    tri.vertices = V2_3D;
	tri.faces = F2;

	return tri;
}


PYBIND11_MODULE(triangulation, m) {
    m.def("triangulate_polygon", &triangulate_polygon, py::arg("V").noconvert(), py::arg("E").noconvert());

    py::class_<Triangulation>(m, "Triangulation")
    	.def_readonly("vertices", &Triangulation::vertices)
    	.def_readonly("faces", &Triangulation::faces);
}
