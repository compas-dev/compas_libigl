import compas
from compas_libigl.mapping import map_mesh
from compas.datastructures import Mesh


def test_map_mesh():
    # Create target mesh (using a mesh we know exists)
    mesh = Mesh.from_off(compas.get("tubemesh.off"))
    mesh.quads_to_triangles()  # Ensure we have a triangle mesh
    v, f = mesh.to_vertices_and_faces()

    # Create simple pattern mesh manually (grid pattern)
    # Use a smaller UV range to ensure pattern falls within target's parameterization
    u_num, v_num = 5, 5
    # Use a smaller central region of the UV space
    u_range = [0.2, 0.8]  # Avoid edges of UV space
    v_range = [0.2, 0.8]  # Avoid edges of UV space

    # Generate grid vertices
    pv = []
    for j in range(v_num + 1):
        v_param = v_range[0] + j * (v_range[1] - v_range[0]) / v_num
        for i in range(u_num + 1):
            u_param = u_range[0] + i * (u_range[1] - u_range[0]) / u_num
            pv.append([u_param, v_param, 0])

    # Create faces (triangulated quads)
    pf = []
    for j in range(v_num):
        for i in range(u_num):
            # Calculate vertex indices for this quad
            v0 = j * (u_num + 1) + i
            v1 = j * (u_num + 1) + i + 1
            v2 = (j + 1) * (u_num + 1) + i + 1
            v3 = (j + 1) * (u_num + 1) + i

            # Split quad into two triangles
            pf.append([v0, v1, v2])
            pf.append([v0, v2, v3])

    # Map pattern onto target mesh
    mv, mf, mn, mb, mg = map_mesh((v, f), (pv, pf))
    mesh_mapped = Mesh.from_vertices_and_faces(mv, mf)

    # Verify the result is a valid mesh
    assert mesh_mapped is not None
    assert mesh_mapped.number_of_vertices() > 0
    assert mesh_mapped.number_of_faces() > 0
    assert isinstance(mesh_mapped, Mesh)

    # Check that at least some faces were mapped
    assert mesh_mapped.number_of_faces() > 0
