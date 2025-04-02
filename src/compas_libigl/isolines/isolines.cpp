#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <igl/isolines.h>

namespace py = pybind11;

using RowMatrixXd = Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;
using RowMatrixXi = Eigen::Matrix<int, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;


struct Isolines {
	RowMatrixXd vertices;
	RowMatrixXi edges;
};


Isolines
trimesh_isolines(
    RowMatrixXd V,
    RowMatrixXi F,
    Eigen::VectorXd z,
    int n)
{
	RowMatrixXd Vi;
	RowMatrixXi Ei;

	igl::isolines(V, F, z, n, Vi, Ei);

	Isolines iso;

	iso.vertices = Vi;
	iso.edges = Ei;

	return iso;
}


PYBIND11_MODULE(compas_libigl_isolines, m) {
    m.def(
        "trimesh_isolines",
        &trimesh_isolines,
        py::arg("V").noconvert(),
        py::arg("F").noconvert(),
        py::arg("z"),
        py::arg("n")
    );

    py::class_<Isolines>(m, "Isolines")
    	.def_readonly("vertices", &Isolines::vertices)
    	.def_readonly("edges", &Isolines::edges);
}
