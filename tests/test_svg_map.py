from pathlib import Path

from mapcolor.svg_map import load_regions, render_colored_svg


def test_loads_rectangles_from_nested_svg_group(tmp_path: Path):
    svg = tmp_path / "map.svg"
    svg.write_text(
        """
        <svg xmlns="http://www.w3.org/2000/svg">
          <metadata>ignored</metadata>
          <g>
            <rect id="left" x="0" y="0" width="10" height="10" />
            <rect id="right" x="10" y="0" width="10" height="10" />
          </g>
        </svg>
        """,
        encoding="utf-8",
    )

    regions = load_regions(svg)

    assert [region.name for region in regions] == ["left", "right"]


def test_renders_colored_svg(tmp_path: Path):
    svg = tmp_path / "map.svg"
    svg.write_text(
        """
        <svg xmlns="http://www.w3.org/2000/svg">
          <rect id="a" x="0" y="0" width="10" height="10" />
        </svg>
        """,
        encoding="utf-8",
    )

    rendered = render_colored_svg(svg, {"a": 1}, colors=("#111111", "#222222"))

    assert 'id="a"' in rendered
    assert 'fill="#222222"' in rendered
