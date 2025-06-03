cmake_minimum_required(VERSION 3.15...3.26)

project(compas_libigl LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)

option(ENABLE_PRECOMPILED_HEADERS "Enable precompiled headers" OFF)
option(MULTITHREADED_COMPILATION "Enable multi-threaded compilation (Ninja only)" ON)

# Set build options
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  message(STATUS "Setting build type to 'Release' as none was specified.")
  set(CMAKE_BUILD_TYPE "Release" CACHE STRING "Choose the type of build." FORCE)
  # Set the possible values of build type for cmake-gui
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS
    "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

# Specify the compiler standard flag
set(CMAKE_CXX_EXTENSIONS OFF)

# Set the use of a pre-compile header
if(MULTITHREADED_COMPILATION)
  include(ProcessorCount)
  ProcessorCount(N)
  if(NOT N EQUAL 0)
    message(STATUS "Using ${N} build jobs.")
    set(CMAKE_PARALLEL_LEVEL ${N})
    if(CMAKE_GENERATOR MATCHES "^Ninja")
      set(CMAKE_JOB_POOL_COMPILE compile)
      set(CMAKE_JOB_POOL_LINK link)
      set(CMAKE_JOB_POOLS
        "compile=${N}"
        "link=2")
    endif()
  endif()
endif()

if(UNIX AND NOT APPLE)
  # Install to share/bin|lib
  if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
    set(CMAKE_INSTALL_PREFIX
        "${CMAKE_INSTALL_PREFIX}/share/${PROJECT_NAME}"
        CACHE PATH "Install prefix" FORCE)
  endif()
endif()

include(ExternalProject)
include(CMakeDependentOption)

# Create directories to store external dependencies
if(NOT DEFINED EXTERNAL_DIR)
    set(EXTERNAL_DIR "${CMAKE_SOURCE_DIR}/external")
endif()
file(MAKE_DIRECTORY ${EXTERNAL_DIR})

# Set source directories for external dependencies
set(EIGEN_SOURCE_DIR "${EXTERNAL_DIR}/eigen")
set(LIBIGL_SOURCE_DIR "${EXTERNAL_DIR}/libigl")
set(CLIPPER2_SOURCE_DIR "${EXTERNAL_DIR}/clipper2")

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

# ------------------------------------------------------------------------------
# Clipper2 (static library)
# ------------------------------------------------------------------------------

# Define paths for Clipper2
set(CLIPPER2_LIB_DIR "${CMAKE_BINARY_DIR}/clipper2_static_lib")
file(MAKE_DIRECTORY ${CLIPPER2_LIB_DIR})
set(CLIPPER2_STATIC_LIB "${CLIPPER2_LIB_DIR}/libClipper2.a")
set(CLIPPER2_INCLUDE_DIR "${CLIPPER2_SOURCE_DIR}/CPP/Clipper2Lib/include")

# Only download Clipper2 if source directory doesn't exist
if(NOT EXISTS "${CLIPPER2_SOURCE_DIR}/CPP/Clipper2Lib/include/clipper2")
    message(STATUS "Downloading clipper2...")
    ExternalProject_Add(
        clipper2_download
        PREFIX ${EXTERNAL_DIR}
        URL https://github.com/AngusJohnson/Clipper2/releases/download/Clipper2_1.5.3/Clipper2_1.5.3.zip
        SOURCE_DIR "${CLIPPER2_SOURCE_DIR}"
        CONFIGURE_COMMAND ""
        BUILD_COMMAND ""
        INSTALL_COMMAND ""
        LOG_DOWNLOAD ON
        UPDATE_COMMAND ""
        PATCH_COMMAND ""
        DOWNLOAD_EXTRACT_TIMESTAMP TRUE
    )
endif()

# Only build Clipper2 if the static library doesn't exist
if(NOT EXISTS "${CLIPPER2_STATIC_LIB}")
    # Custom command to build the Clipper2 static library
    add_custom_command(
        OUTPUT ${CLIPPER2_STATIC_LIB}
        COMMAND ${CMAKE_CXX_COMPILER} -c -fPIC 
            "${CLIPPER2_SOURCE_DIR}/CPP/Clipper2Lib/src/clipper.engine.cpp" 
            "${CLIPPER2_SOURCE_DIR}/CPP/Clipper2Lib/src/clipper.offset.cpp" 
            "${CLIPPER2_SOURCE_DIR}/CPP/Clipper2Lib/src/clipper.rectclip.cpp" 
            -I"${CLIPPER2_SOURCE_DIR}/CPP/Clipper2Lib/include"
        COMMAND ${CMAKE_AR} cr "${CLIPPER2_STATIC_LIB}" clipper.engine.o clipper.offset.o clipper.rectclip.o
        COMMAND ${CMAKE_RANLIB} "${CLIPPER2_STATIC_LIB}"
        WORKING_DIRECTORY ${CLIPPER2_LIB_DIR}
        COMMENT "Building Clipper2 static library"
    )

    # Custom target to trigger the Clipper2 build
    add_custom_target(clipper2_build ALL DEPENDS ${CLIPPER2_STATIC_LIB})
    
    # Make clipper2_build depend on the downloads
    if(TARGET clipper2_download)
        add_dependencies(clipper2_build clipper2_download)
    endif()
    add_dependencies(clipper2_build external_downloads)
else()
    # If the static library already exists, create a dummy target
    add_custom_target(clipper2_build)
endif()

# No additional target needed as clipper2_build is already defined by ExternalProject_Add

# Create a custom target for all external dependencies
add_custom_target(external_downloads ALL)
if(TARGET eigen_download)
    add_dependencies(external_downloads eigen_download)
endif()
if(TARGET libigl_download)
    add_dependencies(external_downloads libigl_download)
endif()
if(TARGET clipper2_download)
    add_dependencies(external_downloads clipper2_download)
endif()

# Add include directories for external dependencies
set(EIGEN_INCLUDE_DIR "${EIGEN_SOURCE_DIR}")
set(LIBIGL_INCLUDE_DIR "${LIBIGL_SOURCE_DIR}/include")
set(CLIPPER2_INCLUDE_DIR "${CLIPPER2_SOURCE_DIR}/CPP/Clipper2Lib/include")

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
   $ pip install --no-build-isolation -ve .
  =====================================================================
  You may optionally add -Ceditable.rebuild=true to auto-rebuild when
  the package is imported. Otherwise, you need to re-run the above
  after editing C++ files.")
endif()

# Find Python and nanobind
find_package(Python 3.8
  REQUIRED COMPONENTS Interpreter Development.Module
  OPTIONAL_COMPONENTS Development.SABIModule)
find_package(nanobind CONFIG REQUIRED)
find_package(Threads REQUIRED)

# Create a shared precompiled header library
if (ENABLE_PRECOMPILED_HEADERS)
    add_library(compas_pch INTERFACE)
    target_precompile_headers(compas_pch INTERFACE src/compas.hpp)
    target_include_directories(compas_pch INTERFACE
        ${EIGEN_INCLUDE_DIR}
        ${LIBIGL_INCLUDE_DIR}
        ${CLIPPER2_INCLUDE_DIR}
    )
endif()

# Function to add a nanobind module with include directories
function(add_nanobind_module module_name source_file)
    nanobind_add_module(${module_name} STABLE_ABI NB_STATIC ${source_file})

    # Ensure external dependencies are downloaded and built first
    add_dependencies(${module_name} external_downloads clipper2_build)

    # Add include directories and link PCH if enabled
    if (ENABLE_PRECOMPILED_HEADERS)
        target_link_libraries(${module_name} PRIVATE compas_pch)
    else()
        target_include_directories(${module_name} SYSTEM PRIVATE
            ${EIGEN_INCLUDE_DIR}
            ${LIBIGL_INCLUDE_DIR}
            ${CLIPPER2_INCLUDE_DIR}
        )
    endif()

    # Link Clipper2 directly using the static library path
    target_link_libraries(${module_name} PRIVATE Threads::Threads ${CLIPPER2_STATIC_LIB})
    
    install(TARGETS ${module_name} LIBRARY DESTINATION compas_libigl)
endfunction()

# Add modules
add_nanobind_module(_nanobind src/nanobind.cpp)
add_nanobind_module(_types_std src/types_std.cpp)
add_nanobind_module(_boundaries src/boundaries.cpp)
add_nanobind_module(_curvature src/curvature.cpp)
add_nanobind_module(_geodistance src/geodistance.cpp)
add_nanobind_module(_intersections src/intersections.cpp)
add_nanobind_module(_isolines src/isolines.cpp)
add_nanobind_module(_massmatrix src/massmatrix.cpp)
add_nanobind_module(_meshing src/meshing.cpp)
add_nanobind_module(_parametrisation src/parametrisation.cpp)
add_nanobind_module(_planarize src/planarize.cpp)
add_nanobind_module(_mapping src/mapping.cpp)

# Install the Clipper2 static library
install(FILES "${CLIPPER2_STATIC_LIB}" 
        DESTINATION lib)

# Install Clipper2 headers
install(DIRECTORY "${CLIPPER2_SOURCE_DIR}/CPP/Clipper2Lib/include/clipper2" 
        DESTINATION include)