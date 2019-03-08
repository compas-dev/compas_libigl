cmake_minimum_required(VERSION 3.12)
project(triangulation)
set(CMAKE_CXX_STANDARD 11)

pybind11_add_module(triangulation MODULE triangulation.cpp)

target_link_libraries(triangulation PRIVATE igl::core)
target_link_libraries(triangulation PRIVATE igl::triangle)

set_target_properties(triangulation PROPERTIES 
		      LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/lib/triangulation")

configure_file(triangulation.py "${CMAKE_SOURCE_DIR}/lib/triangulation/triangulation.py" COPYONLY)