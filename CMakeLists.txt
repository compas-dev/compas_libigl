cmake_minimum_required(VERSION 3.14)

project(compas_libigl)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

set(CPLUS_INCLUDE_PATH "$ENV{HOME}/anaconda3/envs/igl/include")

#Eigen
# add as submodule
# find_package (Eigen3 3.3 REQUIRED)
set(CMAKE_PREFIX_PATH ${CMAKE_CURRENT_SOURCE_DIR}/ext/eigen)

#Boost
if (WIN32)
	set(BOOST_ROOT "$ENV{USERPROFILE}/anaconda3/envs/igl/Library/include")
else ()
	set(BOOST_ROOT "$ENV{HOME}/anaconda3/envs/igl/include")
endif()

#Pybind11
set(PYBIND11_CPP_STANDARD -std=c++11)
set(PYBIND11_PYTHON_VERSION 3.7)
if (WIN32)
	set(PYTHON_EXECUTABLE "$ENV{USERPROFILE}/anaconda3/envs/igl/python.exe")
else ()
	set(PYTHON_EXECUTABLE "$ENV{HOME}/anaconda3/envs/igl/bin/python3.7")
endif()
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/ext/pybind11)

#Libigl
option(LIBIGL_WITH_TRIANGLE "Use Triangle" ON)
option(LIBIGL_WITH_CGAL "Use CGAL" ON)
find_package(LIBIGL REQUIRED)

add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/modules)
