cmake_minimum_required(VERSION 3.14)

add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/planarize)
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/isolines)
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/triangulation)
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/geodistance)

if (WIN32)
    # add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/booleans)
    # add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/csgtree)
else ()
    add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/booleans)
    # add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/csgtree)
endif ()
