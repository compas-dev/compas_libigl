cmake_minimum_required(VERSION 3.14)
project(compas_libigl_geodistance)
set(CMAKE_CXX_STANDARD 11)

pybind11_add_module(compas_libigl_geodistance MODULE geodistance.cpp)

target_link_libraries(compas_libigl_geodistance PRIVATE igl::core)

#set_target_properties(geodistance PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/src/compas_libigl/geodistance")
#set_target_properties(geodistance PROPERTIES LIBRARY_OUTPUT_DIRECTORY_RELEASE "${CMAKE_SOURCE_DIR}/src/compas_libigl/geodistance")
#configure_file(__init__.py "${CMAKE_SOURCE_DIR}/src/compas_libigl/geodistance/__init__.py" COPYONLY)
