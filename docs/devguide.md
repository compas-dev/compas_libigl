# Development guide

COMPAS libigl combines a Python frontend in `src/compas_libigl`, small nanobind extension modules built from `src/*.cpp`, and tests in `tests`.

The project metadata and Python dependencies live in `pyproject.toml`; `uv.lock` records the reproducible development environment; and `CMakeLists.txt` owns native dependencies and extension-module configuration. Generated build products belong in `build` and `dist`, while persistent native dependency sources live in `.third_party`.

- [Development environment](devguide/environment.md)
- [Compiler requirements](devguide/compiler.md)
- [Contributing](devguide/contribute.md)
- [CMake configuration](devguide/cmake_configuration.md)
- [Native type conversion](devguide/types.md)
- [Style](devguide/style.md)
