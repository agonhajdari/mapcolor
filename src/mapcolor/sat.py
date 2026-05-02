from itertools import combinations

from pysat.solvers import Solver

from .graph import edges
from .models import Adjacency, Coloring, RegionName


def solve_coloring(adjacency: Adjacency, color_count: int = 4) -> Coloring | None:
    if color_count < 1:
        raise ValueError("color_count must be at least 1")

    regions = list(adjacency)
    variables = _variables(regions, color_count)

    with Solver(name="g3") as solver:
        for region in regions:
            region_colors = [variables[(region, color)] for color in range(color_count)]
            solver.add_clause(region_colors)
            for first_color, second_color in combinations(region_colors, 2):
                solver.add_clause([-first_color, -second_color])

        for first_region, second_region in edges(adjacency):
            for color in range(color_count):
                solver.add_clause([
                    -variables[(first_region, color)],
                    -variables[(second_region, color)],
                ])

        if not solver.solve():
            return None

        model = set(solver.get_model())
        return {
            region: color
            for (region, color), variable in variables.items()
            if variable in model
        }


def _variables(
    regions: list[RegionName],
    color_count: int,
) -> dict[tuple[RegionName, int], int]:
    return {
        (region, color): region_index * color_count + color + 1
        for region_index, region in enumerate(regions)
        for color in range(color_count)
    }
