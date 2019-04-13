cmake_minimum_required(VERSION 3.12)
project(MeshPattern)
set(CMAKE_CXX_STANDARD 11)
find_package (Eigen3 3.3 REQUIRED)
add_library(MeshPatternLib STATIC iglMesh.cpp)

target_link_libraries(MeshPatternLib PRIVATE igl::core Eigen3::Eigen)
target_include_directories(MeshPatternLib PRIVATE ${EIGEN_INCLUDE_DIR})

pybind11_add_module(MeshPattern MODULE MeshPattern.cpp)
target_link_libraries(MeshPattern PRIVATE MeshPatternLib)

set_target_properties(MeshPattern PROPERTIES
		              LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/lib/MeshPattern")

configure_file(MeshPatternBlender.py "${CMAKE_SOURCE_DIR}/lib/MeshPattern/MeshPatternBlender.py" COPYONLY)