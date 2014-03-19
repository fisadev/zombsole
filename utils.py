#coding: utf-8
import math


def distance(a, b):
    '''Calculates distance between two positions.'''
    x1, y1 = a
    x2, y2 = b

    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return math.sqrt((dx ** 2) + (dy ** 2))


def closest(something, others):
    '''Returns the closest other to something.'''
    if others:
        by_distance = lambda other: distance(something.position,
                                             other.position)
        return sorted(others, key=by_distance)[0]


def possible_moves(position, things):
    '''Calculates the possible moves for a thing.'''
    deltas = ((0, 1),
              (0, -1),
              (1, 0),
              (-1, 0))

    positions = [(position[0] + delta[0],
                  position[1] + delta[1])
                 for delta in deltas]

    positions = [position for position in positions
                 if things.get(position) is None]

    return positions
