class MapColorError(Exception):
    """Base exception for user-facing application errors."""


class SvgMapError(MapColorError):
    """Raised when an SVG cannot be parsed as a supported map."""


class ColoringError(MapColorError):
    """Raised when a valid coloring cannot be produced."""
