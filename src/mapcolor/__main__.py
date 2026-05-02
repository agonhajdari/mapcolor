import argparse
import sys
from pathlib import Path

from .app import color_svg_file
from .errors import MapColorError


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="mapcolor",
        description="Color an SVG map using a SAT-backed four-color solver.",
    )
    parser.add_argument("svg", type=Path, help="Input SVG file to color.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Write the colored SVG to this file instead of stdout.",
    )
    parser.add_argument(
        "--colors",
        type=int,
        default=4,
        help="Number of colors to use from the built-in palette. Defaults to 4.",
    )
    args = parser.parse_args(argv)

    try:
        colored_svg = color_svg_file(args.svg, color_count=args.colors)
    except MapColorError as exc:
        parser.exit(1, f"mapcolor: error: {exc}\n")
    except ValueError as exc:
        parser.exit(1, f"mapcolor: error: {exc}\n")

    if args.output is None:
        print(colored_svg)
    else:
        args.output.write_text(colored_svg + "\n", encoding="utf-8")

    return 0


if __name__ == "__main__":
    sys.exit(main())
