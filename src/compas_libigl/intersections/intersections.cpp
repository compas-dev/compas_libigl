#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>
#include <Eigen/StdVector>
#include <igl/ray_mesh_intersect.h>

namespace py = pybind11;

using RowMatrixXd = Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;
using RowMatrixXi = Eigen::Matrix<int, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;

using Hit = std::tuple<int, float, float, float>;
using HitList = std::vector<Hit>;

HitList
intersection_ray_mesh(
    Eigen::Vector3d point,
    Eigen::Vector3d direction,
    RowMatrixXd V,
    RowMatrixXi F)
{
    HitList hits;
    std::vector<igl::Hit> igl_hits;

	bool result = igl::ray_mesh_intersect(point, direction, V, F, igl_hits);

    if (result) {
        for (const auto& hit : igl_hits) {
            hits.push_back(std::make_tuple(hit.id, hit.u, hit.v, hit.t));
        }
    }

    return hits;
}


PYBIND11_MODULE(compas_libigl_intersections, m) {
    m.def(
        "intersection_ray_mesh",
        &intersection_ray_mesh,
        py::arg("point"),
        py::arg("direction"),
        py::arg("V").noconvert(),
        py::arg("F").noconvert()
    );
}
