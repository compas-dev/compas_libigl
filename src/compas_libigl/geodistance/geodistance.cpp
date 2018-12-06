#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>

#include <igl/exact_geodesic.h>
#include <igl/PI.h>
#include <igl/colormap.h>


Eigen::VectorXd exact(Eigen::MatrixXd V, Eigen::MatrixXi F, int vid) 
{

	Eigen::VectorXd d;
	Eigen::VectorXi VS, FS, VT, FT;

    // Eigen::MatrixXd C;

	VS.resize(1);
	VS << vid;

	VT.setLinSpaced(V.rows(), 0, V.rows() - 1);

	igl::exact_geodesic(V, F, VS, FS, VT, FT, d);

    // // The function should be 1 on each integer coordinate
    // d = (d / strip_size * igl::PI).array().sin().abs().eval();

    // // Compute per-vertex colors
    // igl::colormap(igl::COLOR_MAP_TYPE_INFERNO,d,false,C);

    // Eigen::MatrixXd R(V.rows(), 4);

    // R.col(0) = d;
    // R.col(1) = C.col(0);
    // R.col(2) = C.col(1);
    // R.col(3) = C.col(2);

    // return R;

    return d;
}


Eigen::VectorXd heat() 
{

	

}


PYBIND11_MODULE(geodistance, m) {

    m.def("exact", &exact, "Compute exact geodesic distances.");
    m.def("heat", &heat, "Compute approximate geodesic distances.");

}
