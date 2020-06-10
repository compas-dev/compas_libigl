cmake_minimum_required(VERSION 3.14)
project(compas_libigl)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

#Eigen
if (WIN32)
    set(EIGEN3_INCLUDE_DIR "$ENV{CONDA_PREFIX}/Library/include/eigen3")
else ()
    set(EIGEN3_INCLUDE_DIR "$ENV{CONDA_PREFIX}/include/eigen3")
endif ()

#Boost
if (WIN32)
    set(BOOST_ROOT "$ENV{CONDA_PREFIX}/Library/include")
else ()
    set(BOOST_ROOT "$ENV{CONDA_PREFIX}/include")
endif ()

#Pybind11
set(PYBIND11_CPP_STANDARD -std=c++11)
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/ext/pybind11)

#Libigl
option(LIBIGL_WITH_TRIANGLE "Use Triangle" ON)
option(LIBIGL_WITH_CGAL "Use CGAL" OFF)
find_package(LIBIGL REQUIRED)

#geodistance
pybind11_add_module(compas_libigl_geodistance MODULE ${CMAKE_CURRENT_SOURCE_DIR}/src/compas_libigl/geodistance/geodistance.cpp)
target_link_libraries(compas_libigl_geodistance PRIVATE igl::core)

#isolines
pybind11_add_module(compas_libigl_isolines MODULE ${CMAKE_CURRENT_SOURCE_DIR}/src/compas_libigl/isolines/isolines.cpp)
target_link_libraries(compas_libigl_isolines PRIVATE igl::core)

#planarize
pybind11_add_module(compas_libigl_planarize MODULE ${CMAKE_CURRENT_SOURCE_DIR}/src/compas_libigl/planarize/planarize.cpp)
target_link_libraries(compas_libigl_planarize PRIVATE igl::core)

#triangulation
pybind11_add_module(compas_libigl_triangulation MODULE ${CMAKE_CURRENT_SOURCE_DIR}/src/compas_libigl/triangulation/triangulation.cpp)
target_link_libraries(compas_libigl_triangulation PRIVATE igl::core)
target_link_libraries(compas_libigl_triangulation PRIVATE igl::triangle)

