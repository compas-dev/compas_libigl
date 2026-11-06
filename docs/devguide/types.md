# Native type conversion

The C++ boundary uses Eigen matrices and nanobind. Existing bindings establish the following conventions:

- vertex coordinates use C-contiguous `float64` arrays with shape `(n, 3)`;
- triangle indices use C-contiguous `int32` arrays with shape `(m, 3)`;
- read-only Eigen matrix arguments use `Eigen::Ref<const ...>`;
- compound results use `std::tuple`;
- `std::vector` inputs use const references when no copy is required.

For example:

```cpp
std::tuple<Eigen::MatrixXd, Eigen::MatrixXi> remesh(
    Eigen::Ref<const Eigen::MatrixXd> vertices,
    Eigen::Ref<const Eigen::MatrixXi> faces);
```

Python wrappers should perform only the conversions required by their documented public contract:

```python
vertices = np.asarray(vertices, dtype=np.float64)
faces = np.asarray(faces, dtype=np.int32)
```

Do not add nominal runtime checks or speculative conversion infrastructure. Let NumPy and the native operation enforce ordinary structural preconditions, and check output shapes only where the public contract requires it.

## Static typing contract

Every private native module has a matching `.pyi` file. The stub describes the
exact arrays, sparse matrices, Python containers, defaults, and heterogeneous
tuples exposed by its nanobind functions. Native modules remain private; the
stubs make their boundary verifiable without adding them to the public API.

Public wrappers accept the shared structural aliases from `compas.typing`,
normalize once at the native boundary, and annotate the representation they
actually return. For example, a sparse cotangent matrix is a
`scipy.sparse.csc_matrix`, while a converted principal-curvature result is a
tuple of Python lists. Do not annotate a concrete result with a broad input
alias, convert an array to a list merely for typing, or suppress a native import
with an unqualified type-checker ignore.

Verify the contract with:

```text
python -m pyright
python -m pyright --verifytypes compas_libigl --ignoreexternal
python -m pytest tests/test_native_stubs.py tests/test_verify_native_wheel.py
```

The built-wheel checks require `py.typed`, all 13 native stubs, and all 13
compiled extensions to be present in the same artifact.
