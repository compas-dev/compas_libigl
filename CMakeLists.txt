cmake_minimum_required(VERSION 3.15)

project(compas_libigl)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

set(CPLUS_INCLUDE_PATH "/Users/vanmelet/anaconda3/envs/igl/include")

#Eigen
find_package (Eigen3 3.3 REQUIRED)

#Boost
set(BOOST_ROOT "/Users/vanmelet/anaconda3/envs/igl/include")

#Pybind11
set(PYBIND11_CPP_STANDARD -std=c++11)
set(PYBIND11_PYTHON_VERSION 3.7)
set(PYTHON_EXECUTABLE "$ENV{HOME}/anaconda3/envs/igl/bin/python3.7")
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/ext/pybind11)

#Libigl
option(LIBIGL_WITH_TRIANGLE "Use Triangle" ON)
option(LIBIGL_WITH_CGAL "Use CGAL" ON)
find_package(LIBIGL REQUIRED)

add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/modules)
