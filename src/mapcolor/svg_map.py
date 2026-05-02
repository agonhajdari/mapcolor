import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterable

from collision import Concave_Poly, Poly, Vector

from .errors import SvgMapError
from .models import Coloring, Region

SVG_NAMESPACE = "http://www.w3.org/2000/svg"
DEFAULT_COLORS = ("#FF0000", "#00FF00", "#0000FF", "#FF00FF")


def load_regions(svg_path: str | Path) -> list[Region]:
    tree = _parse_svg(svg_path)
    regions: list[Region] = []

    for element in tree.getroot().iter():
        tag = _local_name(element.tag)
        if tag not in {"polygon", "rect"}:
            continue

        region_id = element.attrib.get("id", "").strip()
        if not region_id:
            raise SvgMapError(f"Supported SVG shape <{tag}> is missing an id")

        if tag == "polygon":
            regions.append(Region(region_id, _polygon_from_element(element)))
        elif tag == "rect":
            regions.append(Region(region_id, _rect_from_element(element)))

    if not regions:
        raise SvgMapError("SVG does not contain any supported <rect> or <polygon> regions")

    return regions


def render_colored_svg(
    svg_path: str | Path,
    coloring: Coloring,
    colors: Iterable[str] = DEFAULT_COLORS,
) -> str:
    tree = _parse_svg(svg_path)
    color_palette = tuple(colors)

    if not color_palette:
        raise SvgMapError("At least one output color is required")

    colored_regions = 0
    for element in tree.getroot().iter():
        if _local_name(element.tag) not in {"polygon", "rect"}:
            continue

        region_id = element.attrib.get("id", "").strip()
        if region_id not in coloring:
            raise SvgMapError(f"No color was assigned to region {region_id!r}")

        color_index = coloring[region_id]
        try:
            element.set("fill", color_palette[color_index])
        except IndexError as exc:
            raise SvgMapError(f"Color index {color_index} is outside the output palette") from exc
        colored_regions += 1

    if colored_regions == 0:
        raise SvgMapError("SVG does not contain any supported <rect> or <polygon> regions")

    ET.register_namespace("", SVG_NAMESPACE)
    return ET.tostring(tree.getroot(), encoding="unicode")


def _parse_svg(svg_path: str | Path) -> ET.ElementTree:
    try:
        return ET.parse(svg_path)
    except ET.ParseError as exc:
        raise SvgMapError(f"Invalid SVG XML: {exc}") from exc
    except OSError as exc:
        raise SvgMapError(f"Could not read SVG {str(svg_path)!r}: {exc}") from exc


def _polygon_from_element(element: ET.Element) -> Concave_Poly:
    raw_points = element.attrib.get("points", "")
    points = _parse_points(raw_points)
    return Concave_Poly(Vector(0, 0), points)


def _rect_from_element(element: ET.Element) -> Poly:
    x = _float_attr(element, "x", default=0.0)
    y = _float_attr(element, "y", default=0.0)
    width = _float_attr(element, "width")
    height = _float_attr(element, "height")

    top_left = Vector(x, y)
    top_right = top_left + Vector(width, 0)
    bottom_right = top_left + Vector(width, height)
    bottom_left = top_left + Vector(0, height)
    return Poly(Vector(0, 0), [top_left, top_right, bottom_right, bottom_left])


def _parse_points(raw_points: str) -> list[Vector]:
    values = [value for value in re.split(r"[\s,]+", raw_points.strip()) if value]
    if len(values) < 6 or len(values) % 2 != 0:
        raise SvgMapError(f"Invalid polygon points: {raw_points!r}")

    try:
        coordinates = [float(value) for value in values]
    except ValueError as exc:
        raise SvgMapError(f"Invalid polygon coordinate in {raw_points!r}") from exc

    return [
        Vector(coordinates[index], coordinates[index + 1])
        for index in range(0, len(coordinates), 2)
    ]


def _float_attr(element: ET.Element, attr: str, default: float | None = None) -> float:
    raw_value = element.attrib.get(attr)
    if raw_value is None:
        if default is not None:
            return default
        raise SvgMapError(f"<{_local_name(element.tag)}> is missing required attribute {attr!r}")

    try:
        return float(raw_value)
    except ValueError as exc:
        raise SvgMapError(f"Invalid numeric value for attribute {attr!r}: {raw_value!r}") from exc


def _local_name(tag: str) -> str:
    return tag.rsplit("}", maxsplit=1)[-1]
