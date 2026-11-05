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
