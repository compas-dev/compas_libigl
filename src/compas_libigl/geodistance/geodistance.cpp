#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>

#include <igl/exact_geodesic.h>


Eigen::VectorXd exact(Eigen::MatrixXd V, Eigen::MatrixXi F, int vid) 
{

	Eigen::VectorXd d;
	Eigen::VectorXi VS, FS, VT, FT;

	VS.resize(1);
	VS << vid;

	VT.setLinSpaced(V.rows(), 0, V.rows() - 1);

	igl::exact_geodesic(V, F, VS, FS, VT, FT, d);

	return d;

}


// Eigen::VectorXd heat() {

// }


PYBIND11_MODULE(geodistance, m) {

    m.def("exact", &exact, "Compute exact geodesic distances.");
    // m.def("heat", &heat, "Compute approximate geodesic distances.");

}
