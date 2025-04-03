********************************************************************************
CMake Configuration
********************************************************************************

This project uses CMake with scikit-build-core and nanobind for building Python extensions.

Core Settings
=============

.. code-block:: cmake

    set(CMAKE_CXX_STANDARD 20)
    set(CMAKE_CXX_STANDARD_REQUIRED ON)

External Dependencies
=====================

We use CMake's ExternalProject to manage external dependencies (libigl, Eigen) as header-only libraries. This approach:

1. Downloads dependencies at configure time
2. Extracts them to the ``external`` directory
3. Sets them up as header-only libraries
4. Requires no system-wide installation

Configuration
-------------

.. code-block:: cmake

    # Define source directories
    set(EXTERNAL_DIR "${CMAKE_CURRENT_SOURCE_DIR}/external")
    set(LIBIGL_SOURCE_DIR "${EXTERNAL_DIR}/libigl")
    set(EIGEN_SOURCE_DIR "${EXTERNAL_DIR}/eigen")

    # Create target for all downloads
    add_custom_target(external_downloads ALL)

Example: libigl Setup
---------------------

.. code-block:: cmake

    if(NOT EXISTS "${LIBIGL_SOURCE_DIR}")
        message(STATUS "Downloading libigl...")
        ExternalProject_Add(
            libigl_download
            GIT_REPOSITORY https://github.com/libigl/libigl.git
            GIT_TAG v2.5.0
            SOURCE_DIR       "${LIBIGL_SOURCE_DIR}"
            CONFIGURE_COMMAND ""
            BUILD_COMMAND     ""
            INSTALL_COMMAND   ""
            LOG_DOWNLOAD ON
        )
        add_dependencies(external_downloads libigl_download)
    endif()

Key Components
---------------

* ``SOURCE_DIR``: Where to extract the downloaded files
* Empty ``CONFIGURE_COMMAND``, ``BUILD_COMMAND``, ``INSTALL_COMMAND``: Treat as header-only
* ``LOG_DOWNLOAD ON``: Enable download progress logging
* ``add_dependencies``: Ensure downloads complete before building

Include Directories
-------------------

After download, headers are made available through:

.. code-block:: cmake

    include_directories(
        ${LIBIGL_SOURCE_DIR}/include
        ${EIGEN_SOURCE_DIR}
    )

Build Flags
-----------

Dependencies are configured with specific compiler flags:

.. code-block:: cmake

    # Platform-specific flags
    if(MSVC)
        set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreadedDLL")
        add_definitions(-DNOMINMAX)  # Prevent Windows max/min macro conflicts
    endif()

This setup ensures:
* No compilation of external libraries needed
* Consistent headers across different platforms
* Simplified dependency management
* Reproducible builds
* Proper handling of Windows-specific issues

Precompiled Headers
-------------------

We use precompiled headers to improve build times. The configuration is optimized for template-heavy code:

.. code-block:: cmake

    # Enhanced PCH configuration
    set(CMAKE_PCH_INSTANTIATE_TEMPLATES ON)  # Improve template compilation
    set(CMAKE_PCH_WARN_INVALID ON)          # Warn about invalid PCH usage

    # Configure PCH for the extension
    target_precompile_headers(compas_libigl_ext 
        PRIVATE 
        src/compas.h
    )

Note: When adding new headers that are frequently included, consider adding them to the precompiled header ``src/compas.h`` to further improve build times. Common headers to precompile:

* STL containers (vector, string)
* libigl core headers
* Eigen matrix types
* On Windows, ensure NOMINMAX is defined before any Windows headers
