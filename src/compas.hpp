#pragma once

// Prevent Windows.h from defining min/max macros
#define NOMINMAX

// STL includes
#include <vector>
#include <string>
#include <memory>
#include <algorithm>
#include <cmath>
#include <iostream>
#include <limits>
#include <unordered_map>
#include <tuple>
#include <iomanip>

// Nanobind includes
#include <nanobind/nanobind.h>
#include <nanobind/eigen/dense.h>
#include <nanobind/eigen/sparse.h>
#include <nanobind/stl/tuple.h>
#include <nanobind/stl/vector.h>
#include <nanobind/stl/string.h>

namespace nb = nanobind;

using namespace nb::literals;

// Nanobind type casters: https://nanobind.readthedocs.io/en/latest/exchanging.html

namespace compas {
    // Basic Eigen types with clear naming
    using RowMatrixXd = Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;
    using RowMatrixXi = Eigen::Matrix<int, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;
    using VectorXi = Eigen::VectorXi;
    using VectorXd = Eigen::VectorXd;
    
    // STL containers with descriptive names
    using VectorInt = std::vector<int>;
    using VectorFloat = std::vector<float>;
    using VectorBool = std::vector<bool>;
    using VectorVectorInt = std::vector<VectorInt>;
    
    // Complex types with descriptive names
    using TupleIntFloatFloatFloat = std::tuple<int, float, float, float>;  // face_id, u, v, t
    using VectorTupleIntFloatFloatFloat = std::vector<TupleIntFloatFloatFloat>;
    using VectorVectorTupleIntFloatFloatFloat = std::vector<VectorTupleIntFloatFloatFloat>;
    
    // Tuple types with descriptive names
    using IsolinesResult = std::tuple<RowMatrixXd, RowMatrixXi, RowMatrixXi>;  // vertices, edges, indices
    using RemeshIsolineResult = std::tuple<RowMatrixXd, RowMatrixXi, VectorXi>;  // vertices, faces, labels
    using RemeshIsolinesResult = std::tuple<RowMatrixXd, RowMatrixXi, VectorXd, VectorXi>;  // vertices, faces, scalar_values, face_groups
    using PrincipalCurvatureResult = std::tuple<RowMatrixXd, RowMatrixXd, VectorXd, VectorXd>;  // PD1, PD2, PV1, PV2
    using MeshMapResult = std::tuple<RowMatrixXd, VectorVectorInt, RowMatrixXd, VectorBool, VectorInt>;  // pattern_vertices, pattern_faces, pattern_normals, is_boundary, groups
}