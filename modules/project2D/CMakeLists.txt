cmake_minimum_required(VERSION 3.12)
project(project2D)
set(CMAKE_CXX_STANDARD 11)

pybind11_add_module(project2D MODULE project2D.cpp)

target_link_libraries(project2D PRIVATE igl::core)

set_target_properties(project2D PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/lib/project2D")
