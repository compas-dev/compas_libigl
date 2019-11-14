cmake_minimum_required(VERSION 3.14)
project(planarization)
set(CMAKE_CXX_STANDARD 11)

pybind11_add_module(planarize MODULE planarize.cpp)

target_link_libraries(planarize PRIVATE igl::core)

set_target_properties(planarize PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/src/compas_libigl")

# configure_file(planarize.py "${CMAKE_SOURCE_DIR}/src/compas_libigl/planarize.py" COPYONLY)
# configure_file(tubemesh.json "${CMAKE_SOURCE_DIR}/lib/planarization/tubemesh.json" COPYONLY)
