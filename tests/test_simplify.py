from compas_libigl.simplify import ramer_douglas_peucker


def test_ramer_douglas_peucker():
    # Simple polyline: a zigzag that can be simplified
    points = [
        [0.0, 0.0, 0.0],
        [1.0, 0.1, 0.0],  # slightly off the line
        [2.0, 0.0, 0.0],
        [3.0, 0.05, 0.0],  # slightly off the line
        [4.0, 0.0, 0.0],
    ]
    # With high threshold, should simplify to just endpoints
    S, J, Q = ramer_douglas_peucker(points, threshold=0.5)
    assert len(S) <= len(points)
    assert len(S) >= 2  # At least start and end points
    # With zero threshold, should keep all points
    S2, J2, Q2 = ramer_douglas_peucker(points, threshold=0.0)
    assert len(S2) == len(points)


def test_ramer_douglas_peucker_straight_line():
    # Perfectly straight line should simplify to 2 points
    points = [
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [2.0, 0.0, 0.0],
        [3.0, 0.0, 0.0],
        [4.0, 0.0, 0.0],
    ]
    S, J, Q = ramer_douglas_peucker(points, threshold=0.01)
    assert len(S) == 2
    assert S[0] == [0.0, 0.0, 0.0]
    assert S[1] == [4.0, 0.0, 0.0]
