from .layout import Layout
from .point import Point
from .hex import Hex
from math import pi, cos, sin
import pygame
from .constants import (
    LAYOUT,
    WIN,
    BLUE,
    black_ant,
    black_spider,
    black_queen,
    black_grasshopper,
    black_beetle,
    white_ant,
    white_spider,
    white_queen,
    white_grasshopper,
    white_beetle,
)


def hex_to_pixel(layout: Layout, h: Hex) -> Point:
    m = layout.orientation
    x = (m.f[0] * h.q + m.f[1] * h.r) * layout.size.x
    y = (m.f[2] * h.q + m.f[3] * h.r) * layout.size.y
    return Point(x, y) + layout.origin


def hex_round(coordinates: tuple[float]) -> Hex:
    """rounds hex coordinates

    Args:
        coordinates (tuple[float]): (q, r, s)

    Returns:
        Hex: Hex object having rounded hex coordinates
    """
    q = int(round(coordinates[0]))
    r = int(round(coordinates[1]))
    s = int(round(coordinates[2]))

    q_diff = abs(q - coordinates[0])
    r_diff = abs(r - coordinates[1])
    s_diff = abs(s - coordinates[2])

    if q_diff > r_diff and q_diff > s_diff:
        q = -r - s
    elif r_diff > s_diff:
        r = -q - s
    else:
        s = -q - r

    return Hex(q, r)


def pixel_to_hex(layout: Layout, p: tuple[int, int]) -> Hex:
    """Returns the center of the hexagonal we currently are at

    Args:
        layout (Layout): Use the constant LAYOUT_FLAT
        p (Point): point clicked by mouse down button

    Returns:
        Hex: center of the hex we are currently at
    """
    m = layout.orientation
    pt = Point(
        ((p[0] - layout.origin.x) / layout.size.x),
        ((p[1] - layout.origin.y) / layout.size.y),
    )
    q = m.b[0] * pt.x + m.b[1] * pt.y
    r = m.b[2] * pt.x + m.b[3] * pt.y
    return hex_round((q, r, -q - r))


def hex_corner_offset(layout: Layout, corner: int) -> Point:
    size = layout.size
    # layout.orientation.start_angle == 0 to make it flat top
    angle = 2.0 * pi * (layout.orientation.start_angle + corner) / 6.0
    return Point(size.x * cos(angle), size.y * sin(angle))


def polygon_corners(layout: Layout, h: Hex) -> list[Point]:
    corners = []
    center = hex_to_pixel(layout, h)
    for i in range(6):
        offset = hex_corner_offset(layout, i)
        # print(f"\n\n{offset}\n\n{center}\n\n")
        corners.append(Point(center.x + offset.x, center.y + offset.y))
    return corners


def draw_hex(
    hex: Hex, color: tuple[int] = BLUE, layout: Layout = LAYOUT, WIN=WIN, width=1
):
    """Draw a single Hexagon on the screen."""
    corners = polygon_corners(layout, hex)
    points = [(corner.x, corner.y) for corner in corners]
    pygame.draw.polygon(WIN, color, points, width)


def draw_pieces():

    # Define positions for black pieces (left side)

    black_positions = [
        (50, 50),
        (50, 150),
        (50, 250),
        (50, 350),
        (50, 450),
    ]

    # Define positions for white pieces (right side)
    white_positions = [
        (700, 50),
        (700, 150),
        (700, 250),
        (700, 350),
        (700, 450),
    ]

    # Draw black pieces
    WIN.blit(black_ant, black_positions[0])
    WIN.blit(black_spider, black_positions[1])
    WIN.blit(black_queen, black_positions[2])
    WIN.blit(black_grasshopper, black_positions[3])
    WIN.blit(black_beetle, black_positions[4])

    # Draw white pieces
    WIN.blit(white_ant, white_positions[0])
    WIN.blit(white_spider, white_positions[1])
    WIN.blit(white_queen, white_positions[2])
    WIN.blit(white_grasshopper, white_positions[3])
    WIN.blit(white_beetle, white_positions[4])
