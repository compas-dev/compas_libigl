# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.7.3] 2025-06-25

### Added

### Changed

### Removed


## [0.7.2] 2025-06-24

### Added

### Changed

### Removed

* Removed all the types_std imports from the code. Instead type casters are used: https://nanobind.readthedocs.io/en/latest/exchanging.html .


## [0.7.1] 2025-06-24

### Added

### Changed

* Changed location of `TESSAGON_TYPES` to `compas_libigl.mapping.TESSAGON_TYPES`.
* Changed nanobind types import, from individual types to a single module import.

### Removed


## [0.7.0] 2025-06-04

### Added

- Added simplified borders to map_mesh function.
- Added fixed points to map_mesh function.

### Changed

- Fixed point welding bug in map_mesh function.
- Changed example_isolines to work with the new compas_viewer.
- GA for cibuildwheel, bring back the tessagon test.
- Fixed planarize method to handle triangles.

### Removed


## [0.6.0] 2025-06-04

### Added

- Added map_pattern_to_mesh function.

### Changed

- Changed map_mesh pattern to output more detailed information about the mapping: vertices, faces, normals, boundaries, group indices.
- Changed examples and test to use new map_mesh function.

### Removed


## [0.5.0] 2025-04-18

### Added

* Added Clipper2 to CMakeLists.txt

### Changed

* Mapping method crops the pattern mesh to the boundaries of the target mesh.

### Removed

* Removed all the modules from __init__.py

## [0.4.0] 2025-04-05

### Added

* Add mesh_map using barycentric coordinates.
* Add tessagon for mesh_map example.

### Changed

### Removed

## [0.3.1] 2025-04-01

### Added

### Changed

* Pybind11 build system was updated to Nanobind.
* Github actions workflow was updated for pypi support.
* Documentation was updated to build without errors.

### Removed


## [0.3.1] 2023-12-05

### Added

### Changed

### Removed


## [0.3.0] 2023-12-05

### Added

### Changed

### Removed


## [0.2.5] 2023-12-05

### Added

### Changed

### Removed


## [0.2.4] 2023-12-05

### Added

### Changed

### Removed


## [0.2.3] 2023-11-23

### Added

### Changed

### Removed


## [0.2.2] 2023-11-22

### Added

### Changed

### Removed


## [0.2.1] 2023-11-22

### Added

### Changed

### Removed


## [0.2.0] 2023-11-22

### Added

### Changed

### Removed
