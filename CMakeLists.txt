cmake_minimum_required(VERSION 3.14)
project(compas_libigl)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

#Python
get_filename_component(PYTHON_DIR ${PYTHON_EXECUTABLE} DIRECTORY)
if (NOT WIN32)
    # on OSX the executable is in "bin"
    # so go one more level up
    get_filename_component(PYTHON_DIR ${PYTHON_DIR} DIRECTORY)
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
set(PYBIND11_CPP_STANDARD -std=c++14)
find_package(pybind11 REQUIRED)

#Libigl
option(LIBIGL_WITH_TRIANGLE "Use Triangle" ON)
if (WIN32)
    option(LIBIGL_WITH_CGAL "Use CGAL" OFF)
else ()
    option(LIBIGL_WITH_CGAL "Use CGAL" ON)
endif ()
find_package(LIBIGL REQUIRED)

#booleans
if (NOT WIN32)
    pybind11_add_module(compas_libigl_booleans MODULE ${CMAKE_CURRENT_SOURCE_DIR}/src/compas_libigl/booleans/booleans.cpp)
    target_link_libraries(compas_libigl_booleans PRIVATE igl::core)
    target_link_libraries(compas_libigl_booleans PRIVATE igl::cgal)
endif()

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
