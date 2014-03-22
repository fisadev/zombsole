# coding: utf-8
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


def adyacent_positions(position):
    '''Calculates the 4 adyacent positions of a position.'''
    deltas = ((0, 1),
              (0, -1),
              (1, 0),
              (-1, 0))

    return [(position[0] + delta[0],
             position[1] + delta[1])
            for delta in deltas]


def possible_moves(position, things):
    '''Calculates the possible moves for a thing.'''
    positions = [position for position in adyacent_positions(position)
                 if things.get(position) is None]

    return positions
