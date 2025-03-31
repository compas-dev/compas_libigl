cmake_minimum_required(VERSION 3.15...3.26)

project(nanobind_example LANGUAGES CXX)

include(ExternalProject)

# Define source directories for external dependencies
set(EXTERNAL_DIR "${CMAKE_CURRENT_SOURCE_DIR}/external")
set(EIGEN_SOURCE_DIR "${EXTERNAL_DIR}/eigen")
set(LIBIGL_SOURCE_DIR "${EXTERNAL_DIR}/libigl")
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3")
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g")

# Create a custom target for all external dependencies
add_custom_target(external_downloads ALL)

# Download and configure Eigen
if(NOT EXISTS "${EIGEN_SOURCE_DIR}")
    message(STATUS "Downloading Eigen...")
    ExternalProject_Add(
        eigen_download
        URL https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.gz
        SOURCE_DIR "${EIGEN_SOURCE_DIR}"
        CONFIGURE_COMMAND ""
        BUILD_COMMAND ""
        INSTALL_COMMAND ""
        LOG_DOWNLOAD ON
        UPDATE_COMMAND ""
        PATCH_COMMAND ""
    )
    add_dependencies(external_downloads eigen_download)
endif()

# Download and configure libigl
if(NOT EXISTS "${LIBIGL_SOURCE_DIR}")
    message(STATUS "Downloading libigl...")
    ExternalProject_Add(
        libigl_download
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

# Find Python and nanobind
find_package(Python 3.8
  REQUIRED COMPONENTS Interpreter Development.Module
  OPTIONAL_COMPONENTS Development.SABIModule)
find_package(nanobind CONFIG REQUIRED)
find_package(Threads REQUIRED)

# Add nanobind module
nanobind_add_module(
  nanobind_example_ext
  STABLE_ABI
  NB_STATIC
  src/nanobind_example_ext.cpp
)

# Add dependencies and include directories
add_dependencies(nanobind_example_ext external_downloads)
target_include_directories(nanobind_example_ext PRIVATE 
    ${EIGEN_INCLUDE_DIR}
    ${LIBIGL_INCLUDE_DIR}
)
target_link_libraries(nanobind_example_ext PRIVATE Threads::Threads)

# Install directive for scikit-build-core
install(TARGETS nanobind_example_ext LIBRARY DESTINATION nanobind_example)
