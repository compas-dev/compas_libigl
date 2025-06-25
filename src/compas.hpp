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

// Nanobind type casters: https://nanobind.readthedocs.io/en/latest/exchanging.html
// If you want to bind a vector on your own, do not include compas.h, it will conflict with nanobind stl bindings.
#include <nanobind/nanobind.h>
#include <nanobind/eigen/dense.h>
#include <nanobind/eigen/sparse.h>
#include <nanobind/stl/tuple.h>
#include <nanobind/stl/vector.h>
#include <nanobind/stl/string.h>
 
// Avoid any alias via using, unless really needed:
namespace nb = nanobind;
using namespace nb::literals;

namespace compas {
    // Row-major matrix types for better interoperability with Python numpy arrays
    using RowMatrixXd = Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;
    using RowMatrixXi = Eigen::Matrix<int, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;
    
    // Vector types that maintain row-major storage for consistency
    using RowVectorXd = Eigen::Matrix<double, 1, Eigen::Dynamic, Eigen::RowMajor>;
    using RowVectorXi = Eigen::Matrix<int, 1, Eigen::Dynamic, Eigen::RowMajor>;
}