import math
from ... import effect
from ... import util
from ... import globals as gb
import pygame

class Smoke:
    def __init__(self, x: float, y: float, size: float, sizeIn: float,
                 angle: float, angleIn, alpha: float, alphaRe: float, vAngle, velocity, color: tuple[int, int, int] | list[int]):
        self.x = x
        self.y = y
        self.size = size
        self.sizeIn = sizeIn
        self.angle = angle
        self.angleIn = angleIn
        self.alpha = alpha
        self.alphaRe = alphaRe
        self.color = color
        self.vAngle = vAngle
        self.velocity = velocity

        
class SmokeEffect(effect.Effect):
    sprite = pygame.image.load(gb.baseDir + "/modules/core/assets/bodies/Smoke.png")

    def __init__(self):
        super(SmokeEffect, self).__init__("SmokeEffect")
        
        self.smoke: list[Smoke] = []

    def addSmoke(self, other: Smoke):
        self.smoke.append(other)

    def update(self):
        i = 0
        l = len(self.smoke)

        while (i != l):
            obj = self.smoke[i]

            obj.x += math.cos(obj.vAngle) * obj.velocity
            obj.y += math.sin(obj.vAngle) * obj.velocity

            obj.alpha = max(0, obj.alpha - obj.alphaRe)
            obj.velocity *= .99
            obj.angle += obj.angleIn
            obj.size += obj.sizeIn

            if (obj.alpha < .01):
                self.smoke.pop(i)
                i -= 1
                l -= 1
            i += 1

    def foreGroundDraw(self):
        for i in self.smoke:
            SmokeEffect.sprite.set_alpha(i.alpha)
            
            util.blitRotate(gb.display, pygame.transform.scale(SmokeEffect.sprite, (i.size, i.size)), (i.x, i.y), (i.size / 2, i.size / 2), i.angle * 180 / math.pi)

SmokeEffect()   
