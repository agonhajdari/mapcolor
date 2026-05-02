from pathlib import Path

from .graph import build_adjacency
from .models import Coloring, Region
from .sat import solve_coloring
from .svg_map import load_regions, render_colored_svg


WrapFig = Region


def all_figures(svg: str | Path = "in.svg") -> list[Region]:
    return load_regions(svg)


def intersecting_figures(figures: list[Region]):
    return build_adjacency(figures)


def build_cnf(adj) -> Coloring | None:
    return solve_coloring(adj)


def color_svg(svg: str | Path = "in.svg", coloring: Coloring | None = None) -> None:
    if coloring is None:
        coloring = build_cnf(intersecting_figures(all_figures(svg)))

    print(render_colored_svg(svg, coloring))
