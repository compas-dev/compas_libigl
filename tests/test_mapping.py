import compas
import compas_libigl as igl
from compas.datastructures import Mesh
from tessagon.adaptors.list_adaptor import ListAdaptor
from tessagon.types.hex_tessagon import HexTessagon


def test_map_mesh():
    # Create target mesh (using a mesh we know exists)
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    mesh.quads_to_triangles()  # Ensure we have a triangle mesh
    v, f = mesh.to_vertices_and_faces()

    # Create simple pattern mesh
    options = {
        "function": lambda u, v: [u, v, 0],
        "u_range": [0, 1.0],
        "v_range": [0, 1.0],
        "u_num": 4,  # Small number for fast test
        "v_num": 3,  # Small number for fast test
        "u_cyclic": False,
        "v_cyclic": False,
        "adaptor_class": ListAdaptor,
    }
    tessagon = HexTessagon(**options)
    tessagon_mesh = tessagon.create_mesh()
    pv = tessagon_mesh["vert_list"]
    pf = tessagon_mesh["face_list"]

    # Map pattern onto target mesh
    mv, mf = igl.map_mesh((v, f), (pv, pf))
    mesh_mapped = Mesh.from_vertices_and_faces(mv, mf)

    # Verify the result is a valid mesh
    assert mesh_mapped is not None
    assert mesh_mapped.number_of_vertices() > 0
    assert mesh_mapped.number_of_faces() > 0
    assert isinstance(mesh_mapped, Mesh)

    # Check that at least some faces were mapped
    assert mesh_mapped.number_of_faces() > 0
