#coding: utf-8
import math


def get_position(something):
    '''Gets the position of something (thing, coordinates, ...)'''
    if hasattr(something, 'position'):
        return something.position
    elif isinstance(something, tuple):
        return something


def distance(a, b):
    '''Calculates distance between two things/positions.'''
    x1, y1 = get_position(a)
    x2, y2 = get_position(b)

    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return math.sqrt((dx ** 2) + (dy ** 2))


def closest(self, others):
    '''Returns the closest other to self.'''
    if others:
        return sorted(others, lambda x: distance(self, x))[0]
