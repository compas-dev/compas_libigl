cmake_minimum_required(VERSION 3.14)
project(scgtree)
set(CMAKE_CXX_STANDARD 11)

pybind11_add_module(csgtree MODULE csgtree.cpp)

target_link_libraries(csgtree PRIVATE igl::core)
target_link_libraries(csgtree PRIVATE igl::cgal)

set_target_properties(csgtree PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/src/compas_libigl")
