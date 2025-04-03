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

// Nanobind includes
#include <nanobind/nanobind.h>
#include <nanobind/eigen/dense.h>
#include <nanobind/eigen/sparse.h>
#include <nanobind/stl/tuple.h>
#include <nanobind/stl/bind_vector.h>
#include <nanobind/stl/string.h>

namespace compas {
    using RowMatrixXd = Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;
    using RowMatrixXi = Eigen::Matrix<int, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;
}

namespace nb = nanobind;

using namespace nb::literals;