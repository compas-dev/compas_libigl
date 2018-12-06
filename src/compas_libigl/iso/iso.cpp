#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>

#include <igl/isolines.h>

namespace py = pybind11;

using RowMatrixXd = Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;
using RowMatrixXi = Eigen::Matrix<int, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;

// using RefRowMatrixXd = Eigen::Ref<RowMatrixXd>;
// using RefRowMatrixXi = Eigen::Ref<RowMatrixXi>;


struct Result {
	RowMatrixXd vertices;
};


Result isolines(RowMatrixXd V, RowMatrixXi F, Eigen::VectorXd z, int n)
{
	RowMatrixXd Vi;
	RowMatrixXi Ei;

	igl::isolines(V, F, z, n, Vi, Ei);

	Result result;

	result.vertices = Vi;

	return result;
}


using namespace pybind11::literals;

PYBIND11_MODULE(iso, m) {
    m.def("isolines", &isolines, "V"_a.noconvert(), "F"_a.noconvert(), "z"_a, "n"_a);
}
