# CMake configuration

The project uses scikit-build-core, CMake, and nanobind to build one stable-ABI extension for each native module. The extensions use C++20.

CMake populates native sources under `.third_party` with `FetchContent`:

- Eigen 3.4.0, verified by SHA-256;
- libigl commit `b41f1944a703653ae0da81e6588650ba14c270ea`;
- Clipper2 1.5.3, verified by SHA-256.

These immutable identities make clean builds reproducible. Existing `.third_party/*-src` directories are reused for local builds, but a clean build is the authoritative integrity check.

Each binding has a small C++ source file and a corresponding module declaration:

```cmake
add_nanobind_module(_new_module src/new_module.cpp)
```

The helper links Threads and Clipper2, enables the stable Python ABI, and installs the resulting library into `compas_libigl`. Precompiled headers and Ninja parallelism can be controlled with the `ENABLE_PRECOMPILED_HEADERS` and `MULTITHREADED_COMPILATION` CMake options.
