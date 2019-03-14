cmake_minimum_required(VERSION 3.12)
project(iso)
set(CMAKE_CXX_STANDARD 11)

pybind11_add_module(iso MODULE iso.cpp)

target_link_libraries(iso PRIVATE igl::core)

set_target_properties(iso PROPERTIES 
		      LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/lib/isolines")

configure_file(iso.py "${CMAKE_SOURCE_DIR}/lib/isolines/iso.py" COPYONLY)
configure_file(tubemesh.json "${CMAKE_SOURCE_DIR}/lib/isolines/tubemesh.json" COPYONLY)