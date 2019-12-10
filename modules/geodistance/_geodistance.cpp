#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/eigen.h>
#include <pybind11/numpy.h>
#include <igl/avg_edge_length.h>
#include <igl/exact_geodesic.h>
#include <igl/heat_geodesics.h>
#include <string>

using RowMatrixXd = Eigen::Matrix<double,Eigen::Dynamic,Eigen::Dynamic,Eigen::RowMajor>;
using RowMatrixXi = Eigen::Matrix<int,Eigen::Dynamic,Eigen::Dynamic,Eigen::RowMajor>;
using string = std::string;

class HeatObject {

public:

    // Let's say that a compas mesh had functions that return the vertices and faces as
    // numpy arrays (with the correct data types and format), then we could directly
    // operate on those arrays, by passing them to this function which accepts a
    // Eigen::Ref of the matrix in the right storage order.
    // Since the binding (at the bottom of this file) adds a ".noconvert()" option
    // to those arguments, we make sure that this method call rather fails than
    // copy the data of the matrices.
    void setMesh(Eigen::Ref<RowMatrixXd>V, Eigen::Ref<RowMatrixXi>F) {
        // Note that here, we actually do copy the data, but we could also work
        // on the references directly (unfortunately the igl functions used here
        // do not take Eigen::Ref as arguments)

        m_V = V;
        m_F = F;
    }

    // Since the compas mesh doesn't provide the numpy arrays mentioned above,
    // here is an example which shows how the comopas mesh object could still be accessed
    // from within C++. Note that this is inefficient, and the conversion on python side
    // would be faster, but it shows how far a python object can be pushed into C++
    // code.
    void setMeshCompas(const pybind11::object&compas_mesh) {

        pybind11::object numpy = pybind11::module::import("numpy");

        // Get vertex list as python list
        pybind11::list verts = compas_mesh.attr("get_vertices_attributes")(pybind11::str("xyz"));

        // Create face list as python list
        pybind11::dict key_index = compas_mesh.attr("key_index")();
        pybind11::list faces;

        // Iterating over python lists in C++:
        int i = 0;
        for (const auto& face: compas_mesh.attr("faces")()) {

            int j = 0;
            pybind11::list vert_list(3);
            for (const auto& key: compas_mesh.attr("face_vertices")(face)){
                vert_list[j++] = key_index[key];
            }

            faces.append(vert_list);
        }

        // Conversion of lists to numpy arrays
        // (Sidenote: the "argument"_a notation didn't work here for me, not sure why)
        pybind11::array_t<double> numpy_verts = numpy.attr("array")(pybind11::arg("object")=verts, pybind11::arg("dtype")=numpy.attr("float64"));
        pybind11::array_t<int> numpy_faces = numpy.attr("array")(pybind11::arg("object")=faces, pybind11::arg("dtype")=numpy.attr("int32"));


        // Explicit conversion of the numpy arrays to Eigen refs:
        Eigen::Ref<RowMatrixXd>eigen_verts = numpy_verts.cast<Eigen::Ref<RowMatrixXd>>();
        Eigen::Ref<RowMatrixXi>eigen_faces = numpy_faces.cast<Eigen::Ref<RowMatrixXi>>();

        setMesh(eigen_verts, eigen_faces);
    }

    // Usually, when references are returned to python, the data is copied and
    // a pointer is created which is handled in python.
    // However, in the bindings (at the bottom of this file), we specify a
    // return value policy which prevents this, and so the return vector data
    // is not copied, but still accessible from python.
    const Eigen::VectorXd& getDistanceExact(int vid) {

        Eigen::VectorXi VS, FS, VT, FT;
        VS.resize(1);
        VS << vid;
        VT.setLinSpaced(m_V.rows(), 0, m_V.rows() - 1);
        igl::exact_geodesic(m_V, m_F, VS, FS, VT, FT, m_result);
        return m_result;
    }

    const Eigen::VectorXd& getDistanceHeat(int vid) {

        Eigen::VectorXi gamma;
        gamma.resize(1);
        gamma << vid;

        igl::HeatGeodesicsData<double> data;

        double t = std::pow(igl::avg_edge_length(m_V, m_F), 2);

        igl::heat_geodesics_precompute(m_V, m_F, t, data);

        m_result.setZero(data.Grad.cols());
        m_result(vid) = 1;

        igl::heat_geodesics_solve(data, gamma, m_result);

        return m_result;
    }

protected:

    Eigen::VectorXd m_result;

private:

    RowMatrixXd m_V;
    RowMatrixXi m_F;

};


using namespace pybind11::literals;

PYBIND11_MODULE(geodistance, m) {

    pybind11::class_<HeatObject, std::shared_ptr<HeatObject>> heatObjBinding(m, "HeatObject");

    heatObjBinding.def(pybind11::init<>())
                  .def("setMesh", &HeatObject::setMesh, "V"_a.noconvert(), "F"_a.noconvert())
                  .def("setMesh", &HeatObject::setMeshCompas, "compas_mesh"_a.noconvert())
                  .def("getDistanceExact", &HeatObject::getDistanceExact, pybind11::return_value_policy::reference_internal)
                  .def("getDistanceHeat", &HeatObject::getDistanceHeat, pybind11::return_value_policy::reference_internal);

}
