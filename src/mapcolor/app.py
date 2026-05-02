from pathlib import Path

from .errors import ColoringError
from .graph import build_adjacency
from .sat import solve_coloring
from .svg_map import DEFAULT_COLORS, load_regions, render_colored_svg


def color_svg_file(svg_path: str | Path, color_count: int = len(DEFAULT_COLORS)) -> str:
    if color_count > len(DEFAULT_COLORS):
        raise ValueError(f"At most {len(DEFAULT_COLORS)} colors are supported by the built-in palette")

    regions = load_regions(svg_path)
    adjacency = build_adjacency(regions)
    coloring = solve_coloring(adjacency, color_count=color_count)

    if coloring is None:
        raise ColoringError(f"Could not color map with {color_count} colors")

    return render_colored_svg(svg_path, coloring, colors=DEFAULT_COLORS[:color_count])
