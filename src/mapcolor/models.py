from dataclasses import dataclass
from typing import Any


RegionName = str
ColorIndex = int
Coloring = dict[RegionName, ColorIndex]
Adjacency = dict[RegionName, set[RegionName]]


@dataclass(frozen=True)
class Region:
    name: RegionName
    figure: Any
