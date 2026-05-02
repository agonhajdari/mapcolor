from mapcolor.sat import solve_coloring


def test_solves_four_color_graph():
    adjacency = {
        "a": {"b", "c", "d"},
        "b": {"a", "c", "d"},
        "c": {"a", "b", "d"},
        "d": {"a", "b", "c"},
    }

    coloring = solve_coloring(adjacency, color_count=4)

    assert coloring is not None
    assert set(coloring) == set(adjacency)
    for region, neighbours in adjacency.items():
        for neighbour in neighbours:
            assert coloring[region] != coloring[neighbour]


def test_returns_none_when_not_enough_colors():
    adjacency = {
        "a": {"b", "c", "d"},
        "b": {"a", "c", "d"},
        "c": {"a", "b", "d"},
        "d": {"a", "b", "c"},
    }

    assert solve_coloring(adjacency, color_count=3) is None


def test_rejects_invalid_color_count():
    try:
        solve_coloring({"a": set()}, color_count=0)
    except ValueError as exc:
        assert "color_count" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
