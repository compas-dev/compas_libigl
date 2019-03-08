cmake_minimum_required(VERSION 3.12)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

#Pybind11
set(PYBIND11_PYTHON_VERSION 3.5.3)
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/ext/pybind11)

#Eigen
find_package (Eigen3 3.3 REQUIRED NO_MODULE)

#Libigl
find_package(LIBIGL REQUIRED QUIET)
option(LIBIGL_WITH_TRIANGLE          "Use Triangle"                 ON)

add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/src)

