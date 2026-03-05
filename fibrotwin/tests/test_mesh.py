from src.mechanics.mesh import create_rect_tri_mesh


def test_mesh_counts():
    nodes, elems = create_rect_tri_mesh(1.0, 1.0, 4, 3)
    assert nodes.shape[0] == 12
    assert elems.shape[0] == 2 * (4 - 1) * (3 - 1)
