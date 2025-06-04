from compas_libigl._nanobind import add


def test_add():
    assert add(1, 2) == 3


print(add(1, 2))
