#include <igl/planarize_quad_mesh.h>

#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>


Eigen::MatrixXd planarize(Eigen::MatrixXd V, Eigen::MatrixXi F)
{
    Eigen::MatrixXd Vplanar;

    igl::planarize_quad_mesh(V, F, 100, 0.005, Vplanar);

    return Vplanar;
}

PYBIND11_MODULE(planarize, m) {

    m.def("planarize", &planarize, "Planarize a quad mesh.");

}
