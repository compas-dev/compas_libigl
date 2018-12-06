#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>

#include <igl/exact_geodesic.h>


using RowMatrixXd = Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;
using RowMatrixXi = Eigen::Matrix<int, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;


Eigen::VectorXd exact(RowMatrixXd V, RowMatrixXi F, int vid) 
{
	Eigen::VectorXd d;
	Eigen::VectorXi VS, FS, VT, FT;

	VS.resize(1);
	VS << vid;

	VT.setLinSpaced(V.rows(), 0, V.rows() - 1);

	igl::exact_geodesic(V, F, VS, FS, VT, FT, d);

    return d;
}


Eigen::VectorXd heat(RowMatrixXd V, RowMatrixXi F, int vid) 
{
	Eigen::VectorXd d;

    return d;
}


using namespace pybind11::literals;

PYBIND11_MODULE(geodistance, m) {
    m.def("exact", &exact, "V"_a.noconvert(), "F"_a.noconvert(), "vid"_a);
    m.def("heat", &heat, "V"_a.noconvert(), "F"_a.noconvert(), "vid"_a);
}
