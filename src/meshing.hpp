#pragma once

#include "compas.hpp"
#include <igl/remesh_along_isoline.h>
#include <igl/facet_components.h>
#include <Eigen/Sparse>

// Function to remesh along a single isoline
std::tuple<
    compas::RowMatrixXd,
    compas::RowMatrixXi,
    Eigen::VectorXi>
trimesh_remesh_along_isoline(
    compas::RowMatrixXd V1,
    compas::RowMatrixXi F1,
    Eigen::VectorXd S1,
    double s);

// Function to remesh along multiple isolines
std::tuple<
    compas::RowMatrixXd,
    compas::RowMatrixXi,
    Eigen::VectorXd>
trimesh_remesh_along_isolines(
    compas::RowMatrixXd V,
    compas::RowMatrixXi F,
    Eigen::VectorXd S,
    Eigen::VectorXd values);
