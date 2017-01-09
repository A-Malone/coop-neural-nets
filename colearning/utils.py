import numpy as np
import pygame

class TeamColors(object):
    """docstring for TeamColours"""
    colors = ('red', 'blue', 'green', 'yellow', 'cyan', 'orange')

    @classmethod
    def get(cls, team):
        return pygame.Color(cls.colors[team % len(cls.colors)])

def clip_to_dim(elem, dim):
    if(not 0 <= elem <= dim):
        return max(min(elem, dim), 0)
    return elem

def clip_array_to_dim(in_vec, dim):
    for ind, elem in enumerate(in_vec):
        if(not 0 <= elem <= dim[ind]):
            in_vec[ind] = max(min(elem, dim[ind]), 0)

def out_of_bounds(in_vec, dim):
    for ind, elem in enumerate(in_vec):
        if(not 0 <= elem <= dim[ind]):
            return True
    return False
