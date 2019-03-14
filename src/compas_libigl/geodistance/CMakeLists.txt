cmake_minimum_required(VERSION 3.12)
project(geodistance)
set(CMAKE_CXX_STANDARD 11)

pybind11_add_module(geodistance MODULE geodistance.cpp)

target_link_libraries(geodistance PRIVATE igl::core)

set_target_properties(geodistance PROPERTIES 
		      LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/lib/geodistance")

configure_file(heat.py "${CMAKE_SOURCE_DIR}/lib/geodistance/heat.py" COPYONLY)
configure_file(exact.py "${CMAKE_SOURCE_DIR}/lib/geodistance/exact.py" COPYONLY)
configure_file(bunny.off "${CMAKE_SOURCE_DIR}/lib/geodistance/bunny.off" COPYONLY)
configure_file(tubemesh.json "${CMAKE_SOURCE_DIR}/lib/geodistance/tubemesh.json" COPYONLY)