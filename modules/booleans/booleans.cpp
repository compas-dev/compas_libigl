#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <igl/copyleft/cgal/mesh_boolean.h>
#include <igl/MeshBooleanType.h>

namespace py = pybind11;

using RowMatrixXd = Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;
using RowMatrixXi = Eigen::Matrix<int, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;

struct Mesh {
	RowMatrixXd vertices;
	RowMatrixXi faces;
};


Mesh mesh_union(RowMatrixXd VA, RowMatrixXi FA, RowMatrixXd VB, RowMatrixXi FB)
{
	RowMatrixXd VC;
	RowMatrixXi FC;

    igl::copyleft::cgal::mesh_boolean(VA, FA, VB, FB, igl::MESH_BOOLEAN_TYPE_UNION, VC, FC);

    Mesh mesh;

    mesh.vertices = VC;
    mesh.faces = FC;

    return mesh;
}


using namespace pybind11::literals;

PYBIND11_MODULE(booleans, m) {
    m.def("mesh_union", &mesh_union, "VA"_a.noconvert(), "FA"_a.noconvert(), "VB"_a.noconvert(), "FB"_a.noconvert());

    py::class_<Mesh>(m, "Mesh")
    	.def_readonly("vertices", &Mesh::vertices)
    	.def_readonly("faces", &Mesh::faces);
}
