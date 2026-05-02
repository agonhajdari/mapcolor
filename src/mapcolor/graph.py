from collections import defaultdict
from itertools import combinations

from collision import collide

from .models import Adjacency, Region


def build_adjacency(regions: list[Region]) -> Adjacency:
    adjacency: Adjacency = defaultdict(set, {region.name: set() for region in regions})

    for first, second in combinations(regions, 2):
        if collide(first.figure, second.figure):
            adjacency[first.name].add(second.name)
            adjacency[second.name].add(first.name)

    return dict(adjacency)


def edges(adjacency: Adjacency) -> set[tuple[str, str]]:
    return {
        tuple(sorted((region, neighbour)))
        for region, neighbours in adjacency.items()
        for neighbour in neighbours
        if region != neighbour
    }
