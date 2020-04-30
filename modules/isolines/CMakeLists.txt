cmake_minimum_required(VERSION 3.14)
project(compas_libigl_isolines)
set(CMAKE_CXX_STANDARD 11)

pybind11_add_module(compas_libigl_isolines MODULE isolines.cpp)

target_link_libraries(compas_libigl_isolines PRIVATE igl::core)

#set_target_properties(isolines PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/src/compas_libigl/isolines")
#set_target_properties(isolines PROPERTIES LIBRARY_OUTPUT_DIRECTORY_RELEASE "${CMAKE_SOURCE_DIR}/src/compas_libigl/isolines")
