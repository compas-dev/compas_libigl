# Style

Python code follows the COMPAS conventions and is checked with Ruff. Public Python docstrings use MkDocs-compatible NumPy style with Markdown content.

C++ code uses:

- `snake_case` for functions and variables;
- `_snake_case` for private data members;
- `UPPER_SNAKE_CASE` for constants;
- `UpperCamelCase` for class and struct names;
- explicit `std::` and `Eigen::` namespaces.

Use Doxygen comments for native declarations when additional explanation is useful:

```cpp
/**
 * @brief Compute a scalar value per mesh vertex.
 * @param[in] vertices Vertex coordinates with shape (n, 3).
 * @param[in] faces Triangle indices with shape (m, 3).
 * @return One value per vertex.
 */
Eigen::VectorXd compute_values(
    Eigen::Ref<const Eigen::MatrixXd> vertices,
    Eigen::Ref<const Eigen::MatrixXi> faces);
```

On Windows, define `NOMINMAX` before including Windows headers when those headers are required.
