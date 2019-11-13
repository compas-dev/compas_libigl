cmake_minimum_required(VERSION 3.12)
project(iso)
set(CMAKE_CXX_STANDARD 11)

pybind11_add_module(isolines MODULE isolines.cpp)

target_link_libraries(isolines PRIVATE igl::core)

set_target_properties(isolines PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/src/compas_libigl")

# configure_file(iso.py "${CMAKE_SOURCE_DIR}/lib/isolines/iso.py" COPYONLY)
# configure_file(tubemesh.json "${CMAKE_SOURCE_DIR}/lib/isolines/tubemesh.json" COPYONLY)
