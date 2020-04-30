cmake_minimum_required(VERSION 3.14)
project(compas_libigl_planarize)
set(CMAKE_CXX_STANDARD 11)

pybind11_add_module(compas_libigl_planarize MODULE planarize.cpp)

target_link_libraries(compas_libigl_planarize PRIVATE igl::core)

#set_target_properties(planarize PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/src/compas_libigl/planarize")
#set_target_properties(planarize PROPERTIES LIBRARY_OUTPUT_DIRECTORY_RELEASE "${CMAKE_SOURCE_DIR}/src/compas_libigl/planarize")
#configure_file(__init__.py "${CMAKE_SOURCE_DIR}/src/compas_libigl/planarize/__init__.py" COPYONLY)
