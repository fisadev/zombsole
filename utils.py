# coding: utf-8
import math


def to_position(something):
    """Converts something (thing/position) to a position tuple."""
    if isinstance(something, tuple):
        return something
    else:
        return something.position


def distance(a, b):
    """Calculates distance between two positions or things."""
    x1, y1 = to_position(a)
    x2, y2 = to_position(b)

    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return math.sqrt((dx ** 2) + (dy ** 2))


def sort_by_distance(something, others):
    by_distance = lambda other: distance(something, other)
    return sorted(others, key=by_distance)


def closest(something, others):
    """Returns the closest other to something (things/positions)."""
    if others:
        return sort_by_distance(something, others)[0]


def adjacent_positions(something):
    """Calculates the 4 adjacent positions of something (thing/position)."""
    position = to_position(something)
    deltas = ((0, 1),
              (0, -1),
              (1, 0),
              (-1, 0))

    return [(position[0] + delta[0],
             position[1] + delta[1])
            for delta in deltas]


def possible_moves(something, things):
    """Calculates the possible moves for a thing."""
    positions = [position for position in adjacent_positions(something)
                 if things.get(position) is None]

    return positions
