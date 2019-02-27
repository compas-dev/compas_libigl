cmake_minimum_required(VERSION 3.12)
project(planarize)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

#Pybind11
set(PYBIND_INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../../ext/pybind11)
add_subdirectory(${PYBIND_INCLUDE_DIR} pybind11)

find_package (Eigen3 3.3 REQUIRED NO_MODULE)

#Libigl
find_package(LIBIGL REQUIRED QUIET)

pybind11_add_module(planarize main.cpp)
target_link_libraries(planarize PRIVATE Eigen3::Eigen)
target_link_libraries(planarize PUBLIC igl::core)