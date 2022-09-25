import pygame

from . import globals as gb


class Effect:
    def __init__(self, id):
        gb.effects[id] = self
        pass

    def update(self):
        ...
        
    def foreGroundDraw(self):
        
        ...

    def backGroundDraw(self):
        ...
    ...