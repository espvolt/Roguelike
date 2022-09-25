import math
from . import hitbox
import sys

class Projectile:
    idCount = -sys.maxsize

    def __init__(self):
        self.hitbox: hitbox.Hitbox = None
        self.id = Projectile.idCount
        
        Projectile.idCount += 1

    def update(self):
        pass

    def draw(self):
        pass

    def addTo(self, dst: dict):
        dst[self.id] = self
