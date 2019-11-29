#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <igl/copyleft/cgal/CSGTree.h>

namespace py = pybind11;

using namespace Eigen;
using namespace igl::copyleft::cgal;

using RowMatrixXd = Matrix<double, Dynamic, Dynamic, RowMajor>;
using RowMatrixXi = Matrix<int, Dynamic, Dynamic, RowMajor>;

struct CSGMesh {
	RowMatrixXd vertices;
	RowMatrixXi faces;
};


CSGMesh mesh_csgtree(RowMatrixXd VA, RowMatrixXi FA,
                     RowMatrixXd VB, RowMatrixXi FB,
                     RowMatrixXd VC, RowMatrixXi FC,
                     RowMatrixXd VD, RowMatrixXi FD,
                     RowMatrixXd VE, RowMatrixXi FE)
{
    CSGTree M = {{{VA, FA}, {VB, FB}, "i"}, {{{VC, FC}, {VD, FD}, "u"}, {VE, FE}, "u"}, "m"};

    CSGMesh mesh;

    mesh.vertices = M.cast_V<RowMatrixXd>();
    mesh.faces = M.F();

    return mesh;
}


using namespace pybind11::literals;

PYBIND11_MODULE(csgtree, m) {
    m.def("mesh_csgtree", &mesh_csgtree, "VA"_a.noconvert(), "FA"_a.noconvert(),
                                         "VB"_a.noconvert(), "FB"_a.noconvert(),
                                         "VC"_a.noconvert(), "FC"_a.noconvert(),
                                         "VD"_a.noconvert(), "FD"_a.noconvert(),
                                         "VE"_a.noconvert(), "FE"_a.noconvert());

    py::class_<CSGMesh>(m, "CSGMesh")
    	.def_readonly("vertices", &CSGMesh::vertices)
    	.def_readonly("faces", &CSGMesh::faces);
}
