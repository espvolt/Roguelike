from ... import effect
from ... import animation
from ... import globals as gb
from ... import util

import math

import sys

class Blood:
    offset = [63, 65]
    def __init__(self, x: float, y: float, angle: float):
        self.animation: animation.Animation = animation.Animation(.015, False, "_core:BLOOD")

        self.x = x
        self.y = y
        self.angle = angle

    def disable(self):
        self.update = lambda: None

    def update(self):
        self.animation.updateAnimation()

        if (self.animation.currentFrame == len(self.animation.frames()) - 1):
            self.disable()

    def draw(self):
        util.blitRotate(gb.display, self.animation.getFrame(), (self.x, self.y), Blood.offset, self.angle * 180 / math.pi)




class BloodEffect(effect.Effect):
    animation.Animation.fromGif(gb.baseDir + "/modules/core/assets/bodies/Blood.gif", "_core:BLOOD")

    def __init__(self):
        super(BloodEffect, self).__init__("BloodEffect")

        self.structs: list[Blood] = []

    def addBlood(self, other: Blood):
        self.structs.append(other)

    def backGroundDraw(self):
        for i in self.structs:
            i.update()
            i.draw()


BloodEffect()
