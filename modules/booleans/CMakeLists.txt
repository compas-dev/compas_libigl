cmake_minimum_required(VERSION 3.14)
project(compas_libigl_booleans)
set(CMAKE_CXX_STANDARD 11)

pybind11_add_module(compas_libigl_booleans MODULE booleans.cpp)

target_link_libraries(compas_libigl_booleans PRIVATE igl::core)
target_link_libraries(compas_libigl_booleans PRIVATE igl::cgal)
