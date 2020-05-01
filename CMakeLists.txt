cmake_minimum_required(VERSION 3.14)
project(compas_libigl)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

#Python
get_filename_component(PYTHON_DIR ${PYTHON_EXECUTABLE} DIRECTORY)
if (NOT WIN32)
    # on OSX the executable is in "bin"
    # so go one more level up
    get_filename_component(PYTHON_DIR ${PYTHON_DIR} DIRECTORY)
endif ()

#Python includes
if (WIN32)
    set(CPLUS_INCLUDE_PATH "${PYTHON_DIR}/Library/include")
else ()
    set(CPLUS_INCLUDE_PATH "${PYTHON_DIR}/include")
endif ()

#Eigen
if (WIN32)
    set(EIGEN3_INCLUDE_DIR "${PYTHON_DIR}/Library/include/eigen3")
else ()
    set(EIGEN3_INCLUDE_DIR "${PYTHON_DIR}/include/eigen3")
endif ()

#Boost
if (WIN32)
    set(BOOST_ROOT "${PYTHON_DIR}/Library/include")
else ()
    set(BOOST_ROOT "${PYTHON_DIR}/include")
endif ()

#Pybind11
set(PYBIND11_CPP_STANDARD -std=c++11)
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/ext/pybind11)

#Libigl
option(LIBIGL_WITH_TRIANGLE "Use Triangle" ON)
option(LIBIGL_WITH_CGAL "Use CGAL" ON)
find_package(LIBIGL REQUIRED)

#COMPAS libigl modules
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/modules)
