cmake_minimum_required(VERSION 3.14)
project(booleans)
set(CMAKE_CXX_STANDARD 11)

pybind11_add_module(booleans MODULE booleans.cpp)

target_link_libraries(booleans PRIVATE igl::core)
target_link_libraries(booleans PRIVATE igl::cgal)

set_target_properties(booleans PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/src/compas_libigl")
