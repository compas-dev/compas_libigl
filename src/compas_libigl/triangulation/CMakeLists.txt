cmake_minimum_required(VERSION 3.12)
project(triangulation)
set(CMAKE_CXX_STANDARD 11)

pybind11_add_module(triangulation triangulation.cpp)
target_include_directories
target_link_libraries(triangulation PRIVATE igl::triangle igl::core)

