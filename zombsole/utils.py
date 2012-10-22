#coding: utf-8
def get_position(something):
    '''Gets the position of something (thing, coordinates, ...)'''
    if hasattr(something, 'position'):
        return something.position
    elif isinstance(something, tuple):
        return something

