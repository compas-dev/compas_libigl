cmake_minimum_required(VERSION 3.15...3.26)
project(compas_libigl LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_EXTENSIONS OFF)

option(ENABLE_PRECOMPILED_HEADERS "Enable precompiled headers" ON)
option(MULTITHREADED_COMPILATION "Enable multi-threaded compilation (Ninja only)" ON)

if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  message(STATUS "Setting build type to 'Release' as none was specified.")
  set(CMAKE_BUILD_TYPE "Release" CACHE STRING "Choose the type of build." FORCE)
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

if(MULTITHREADED_COMPILATION)
  include(ProcessorCount)
  ProcessorCount(N)
  if(NOT N EQUAL 0)
    message(STATUS "Using ${N} build jobs.")
    set(CMAKE_PARALLEL_LEVEL ${N})
    if(CMAKE_GENERATOR MATCHES "^Ninja")
      set(CMAKE_JOB_POOL_COMPILE compile)
      set(CMAKE_JOB_POOL_LINK link)
      set(CMAKE_JOB_POOLS "compile=${N}" "link=2")
    endif()
  endif()
endif()

if(UNIX AND NOT APPLE)
  if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
    set(CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}/share/${PROJECT_NAME}" CACHE PATH "Install prefix" FORCE)
  endif()
endif()

# Use custom directory for 3rd-party dependencies (optional but persistent)
set(FETCHCONTENT_BASE_DIR "${CMAKE_SOURCE_DIR}/.third_party")
set(FETCHCONTENT_QUIET OFF)
set(FETCHCONTENT_UPDATES_DISCONNECTED ON)

include(FetchContent)

# === Eigen ===
# Check if Eigen already exists
set(EIGEN_DIR "${FETCHCONTENT_BASE_DIR}/eigen-src")
if(EXISTS "${EIGEN_DIR}")
  message(STATUS "Using existing Eigen from ${EIGEN_DIR}")
  set(eigen_SOURCE_DIR "${EIGEN_DIR}")
  set(eigen_BINARY_DIR "${FETCHCONTENT_BASE_DIR}/eigen-build")
endif()

FetchContent_Declare(
  eigen
  URL https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.gz
  SOURCE_DIR "${eigen_SOURCE_DIR}"
  BINARY_DIR "${eigen_BINARY_DIR}"
  DOWNLOAD_EXTRACT_TIMESTAMP TRUE
)
FetchContent_MakeAvailable(eigen)

# === libigl ===
# Check if libigl already exists
set(LIBIGL_DIR "${FETCHCONTENT_BASE_DIR}/libigl-src")
if(EXISTS "${LIBIGL_DIR}")
  message(STATUS "Using existing libigl from ${LIBIGL_DIR}")
  set(libigl_SOURCE_DIR "${LIBIGL_DIR}")
  set(libigl_BINARY_DIR "${FETCHCONTENT_BASE_DIR}/libigl-build")
endif()

FetchContent_Declare(
  libigl
  GIT_REPOSITORY https://github.com/libigl/libigl.git
  GIT_TAG main
  SOURCE_DIR "${libigl_SOURCE_DIR}"
  BINARY_DIR "${libigl_BINARY_DIR}"
)
FetchContent_MakeAvailable(libigl)

# === Clipper2 ===
# Check if Clipper2 already exists
set(CLIPPER2_DIR "${FETCHCONTENT_BASE_DIR}/clipper2-src")
if(EXISTS "${CLIPPER2_DIR}")
  message(STATUS "Using existing Clipper2 from ${CLIPPER2_DIR}")
  set(clipper2_SOURCE_DIR "${CLIPPER2_DIR}")
  set(clipper2_BINARY_DIR "${FETCHCONTENT_BASE_DIR}/clipper2-build")
endif()

FetchContent_Declare(
  clipper2
  URL https://github.com/AngusJohnson/Clipper2/releases/download/Clipper2_1.5.3/Clipper2_1.5.3.zip
  SOURCE_DIR "${clipper2_SOURCE_DIR}"
  BINARY_DIR "${clipper2_BINARY_DIR}"
  DOWNLOAD_EXTRACT_TIMESTAMP TRUE
)
FetchContent_MakeAvailable(clipper2)

# Build Clipper2 as a static library
file(GLOB CLIPPER2_SRC "${clipper2_SOURCE_DIR}/CPP/Clipper2Lib/src/*.cpp")

add_library(clipper2_static STATIC ${CLIPPER2_SRC})
target_include_directories(clipper2_static PUBLIC "${clipper2_SOURCE_DIR}/CPP/Clipper2Lib/include")
set_target_properties(clipper2_static PROPERTIES POSITION_INDEPENDENT_CODE ON)

# Install clipper2 static lib and headers if not already installed
set(CLIPPER2_HEADERS_DEST "${CMAKE_INSTALL_PREFIX}/include/clipper2")
if(NOT EXISTS "${CLIPPER2_HEADERS_DEST}")
  message(STATUS "Installing Clipper2 headers and library")
  install(TARGETS clipper2_static ARCHIVE DESTINATION lib)
  install(DIRECTORY "${clipper2_SOURCE_DIR}/CPP/Clipper2Lib/include/clipper2" DESTINATION include)
endif()

# === Include paths ===
set(EIGEN_INCLUDE_DIR ${eigen_SOURCE_DIR})
set(LIBIGL_INCLUDE_DIR ${libigl_SOURCE_DIR}/include)
set(CLIPPER2_INCLUDE_DIR ${clipper2_SOURCE_DIR}/CPP/Clipper2Lib/include)

# === Python & nanobind ===
find_package(Python 3.8 REQUIRED COMPONENTS Interpreter Development.Module OPTIONAL_COMPONENTS Development.SABIModule)
find_package(nanobind CONFIG REQUIRED)
find_package(Threads REQUIRED)

# === Precompiled headers ===
if (ENABLE_PRECOMPILED_HEADERS)
    add_library(compas_pch INTERFACE)
    target_precompile_headers(compas_pch INTERFACE src/compas.hpp)
    target_include_directories(compas_pch INTERFACE
        ${EIGEN_INCLUDE_DIR}
        ${LIBIGL_INCLUDE_DIR}
        ${CLIPPER2_INCLUDE_DIR}
    )
endif()

# === Function to add nanobind modules ===
function(add_nanobind_module module_name source_file)
    nanobind_add_module(${module_name} STABLE_ABI NB_STATIC ${source_file})
    add_dependencies(${module_name} clipper2_static)

    if (ENABLE_PRECOMPILED_HEADERS)
        target_link_libraries(${module_name} PRIVATE compas_pch)
    else()
        target_include_directories(${module_name} SYSTEM PRIVATE
            ${EIGEN_INCLUDE_DIR}
            ${LIBIGL_INCLUDE_DIR}
            ${CLIPPER2_INCLUDE_DIR}
        )
    endif()

    target_link_libraries(${module_name} PRIVATE Threads::Threads clipper2_static)
    install(TARGETS ${module_name} LIBRARY DESTINATION compas_libigl)
endfunction()

# === Add your modules ===
add_nanobind_module(_boundaries src/boundaries.cpp)
add_nanobind_module(_curvature src/curvature.cpp)
add_nanobind_module(_geodistance src/geodistance.cpp)
add_nanobind_module(_intersections src/intersections.cpp)
add_nanobind_module(_isolines src/isolines.cpp)
add_nanobind_module(_mapping src/mapping.cpp)
add_nanobind_module(_meshing src/meshing.cpp)
add_nanobind_module(_massmatrix src/massmatrix.cpp)
add_nanobind_module(_parametrisation src/parametrisation.cpp)
add_nanobind_module(_planarize src/planarize.cpp)

