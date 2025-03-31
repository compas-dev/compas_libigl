cmake_minimum_required(VERSION 3.15...3.26)

project(compas_libigl LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_BUILD_TYPE Release)

# =====================================================================
# Set this flag to ON for developing to reduce build time.
# Set this flag to OFF for publishing for file size reduction.
# =====================================================================
option(ENABLE_PRECOMPILED_HEADERS "Enable precompiled headers for the build" ON)

# =====================================================================
# Set maximum heap size for MSVC
# =====================================================================

if(MSVC)
    set(CMAKE_GENERATOR_PLATFORM x64)
    add_compile_options(/Zm1200) 
endif()

# =====================================================================
# Build size reduction.
# =====================================================================

if (NOT ENABLE_PRECOMPILED_HEADERS)
    set(CMAKE_INTERPROCEDURAL_OPTIMIZATION TRUE)
    if(MSVC)
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /O1") # Optimize for size on MSVC
    else()
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Os") # Optimize for size on GCC/Clang
    endif()
endif()

# =====================================================================
# Dependencies
# =====================================================================
include(ExternalProject)

# Define source directories for external dependencies
set(EXTERNAL_DIR "${CMAKE_CURRENT_SOURCE_DIR}/external")
set(EIGEN_SOURCE_DIR "${EXTERNAL_DIR}/eigen")
set(LIBIGL_SOURCE_DIR "${EXTERNAL_DIR}/libigl")

# Create directories if they don't exist
file(MAKE_DIRECTORY ${EXTERNAL_DIR})
file(MAKE_DIRECTORY ${EIGEN_SOURCE_DIR})
file(MAKE_DIRECTORY ${LIBIGL_SOURCE_DIR})

# Download Eigen first
if(NOT EXISTS "${EIGEN_SOURCE_DIR}/Eigen")
    message(STATUS "Downloading Eigen...")
    ExternalProject_Add(
        eigen_download
        PREFIX ${EXTERNAL_DIR}
        URL https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.gz
        SOURCE_DIR "${EIGEN_SOURCE_DIR}"
        CONFIGURE_COMMAND ""
        BUILD_COMMAND ""
        INSTALL_COMMAND ""
        LOG_DOWNLOAD ON
        UPDATE_COMMAND ""
        PATCH_COMMAND ""
    )
endif()

# Download libigl after Eigen
if(NOT EXISTS "${LIBIGL_SOURCE_DIR}/include/igl")
    message(STATUS "Downloading libigl...")
    ExternalProject_Add(
        libigl_download
        DEPENDS eigen_download
        PREFIX ${EXTERNAL_DIR}
        URL https://github.com/libigl/libigl/archive/refs/heads/main.zip
        SOURCE_DIR "${LIBIGL_SOURCE_DIR}"
        CONFIGURE_COMMAND ""
        BUILD_COMMAND ""
        INSTALL_COMMAND ""
        LOG_DOWNLOAD ON
        UPDATE_COMMAND ""
        PATCH_COMMAND ""
        DOWNLOAD_EXTRACT_TIMESTAMP TRUE
    )
endif()

# Create a custom target for all external dependencies
add_custom_target(external_downloads ALL)
if(TARGET eigen_download)
    add_dependencies(external_downloads eigen_download)
endif()
if(TARGET libigl_download)
    add_dependencies(external_downloads libigl_download)
endif()

# Add include directories for external dependencies
set(EIGEN_INCLUDE_DIR "${EIGEN_SOURCE_DIR}")
set(LIBIGL_INCLUDE_DIR "${LIBIGL_SOURCE_DIR}/include")

if (NOT SKBUILD)
  message(WARNING "\
  This CMake file is meant to be executed using 'scikit-build'. Running
  it directly will almost certainly not produce the desired result. If
  you are a user trying to install this package, please use the command
  below, which will install all necessary build dependencies, compile
  the package in an isolated environment, and then install it.
  =====================================================================
   $ pip install .
  =====================================================================
  If you are a software developer, and this is your own package, then
  it is usually much more efficient to install the build dependencies
  in your environment once and use the following command that avoids
  a costly creation of a new virtual environment at every compilation:
  =====================================================================
   $ pip install nanobind scikit-build-core[pyproject]
   $ pip install --no-build-isolation -ve .
  =====================================================================
  You may optionally add -Ceditable.rebuild=true to auto-rebuild when
  the package is imported. Otherwise, you need to re-run the above
  after editing C++ files.")
endif()

# Enhanced PCH configuration
if (ENABLE_PRECOMPILED_HEADERS)
    set(CMAKE_PCH_INSTANTIATE_TEMPLATES ON)
    set(CMAKE_PCH_WARN_INVALID ON)
endif() 

# Find Python and nanobind
find_package(Python 3.8
  REQUIRED COMPONENTS Interpreter Development.Module
  OPTIONAL_COMPONENTS Development.SABIModule)
find_package(nanobind CONFIG REQUIRED)
find_package(Threads REQUIRED)

# Function to add a nanobind module with include directories
function(add_nanobind_module module_name source_file)
    nanobind_add_module(${module_name} STABLE_ABI NB_STATIC ${source_file})

    # Ensure external dependencies are downloaded first
    add_dependencies(${module_name} external_downloads)

    # Add include directories
    target_include_directories(${module_name} SYSTEM PRIVATE
        ${EIGEN_INCLUDE_DIR}
        ${LIBIGL_INCLUDE_DIR}
    )

    if (ENABLE_PRECOMPILED_HEADERS)
        target_precompile_headers(${module_name} PRIVATE src/compas.hpp)
    endif()

    target_link_libraries(${module_name} PRIVATE Threads::Threads)
    install(TARGETS ${module_name} LIBRARY DESTINATION compas_libigl)
endfunction()

# Add modules
add_nanobind_module(nanobind src/nanobind.cpp)
add_nanobind_module(types_std src/types_std.cpp)
add_nanobind_module(boundaries src/boundaries.cpp)
add_nanobind_module(curvature src/curvature.cpp)
add_nanobind_module(geodistance src/geodistance.cpp)
add_nanobind_module(intersections src/intersections.cpp)
add_nanobind_module(isolines src/isolines.cpp)
add_nanobind_module(massmatrix src/massmatrix.cpp)
add_nanobind_module(meshing src/meshing.cpp)
add_nanobind_module(parametrisation src/parametrisation.cpp)
add_nanobind_module(planarize src/planarize.cpp)
