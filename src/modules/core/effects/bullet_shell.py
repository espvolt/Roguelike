from turtle import color
from ... import globals as gb
from ... import effect
import pygame
from ... import util
import math
from ... import sound
import random
from ... import map

class Shell:
    
    def __init__(self, x: float, y: float, angle: float, length: float, minLength: float, color: tuple, velocity: float, vAngle: float, spinVel: float):
        self.x = x
        self.y = y
        self.angle = angle
        self.length = length
        self.color = color
        self.minLength = minLength
        self.velocity = velocity
        self.vAngle = -(vAngle - 360) % 360
        self.sounds = [pygame.mixer.Sound(gb.baseDir + "/modules/core/assets/weapons/BulletShellSound1.wav"),
                       pygame.mixer.Sound(gb.baseDir + "/modules/core/assets/weapons/BulletShellSound2.wav"),
                       pygame.mixer.Sound(gb.baseDir + "/modules/core/assets/weapons/BulletShellSound3.wav")]
        self.spinVelocity = spinVel



    def draw(self):
        surf = pygame.Surface((self.length, 1))
        surf.fill(self.color)
        surf.set_colorkey((0, 0, 0))
        util.blitRotate(gb.display, surf, (self.x, self.y), (self.length / 2, 1), self.angle)
        


class ShellEffect(effect.Effect):
    def __init__(self):
        super(ShellEffect, self).__init__("ShellEffect")

        self.shells: list[Shell] = []
        self.bgShells: list[Shell] = []

    def appendShell(self, newShell: Shell):
        self.shells.append(newShell)

    def update(self):
        shells = list(self.shells)
        for i, v in enumerate(shells):
            v.length -= 1
            
            vx = math.cos(v.vAngle * math.pi / 180) * v.velocity
            vy = math.sin(v.vAngle * math.pi / 180) * v.velocity
            
            nx, ny, collided = map.doCollision(v.x, v.y, vx, vy, 1)
            
            v.x += nx
            v.y += ny
            v.velocity *= .8
            v.angle += v.spinVelocity

            
            if (v.length <= v.minLength):
                sound.playSoundPos((v.x, v.y), (gb.playerEntity.x, gb.playerEntity.y), 1, random.choice(v.sounds))

                self.bgShells.append(self.shells.pop(i))
                shells.pop(i)
                i -= 1


    def foreGroundDraw(self):
        for i in self.shells:
            i.draw()

    def backGroundDraw(self):
        for i in self.bgShells:
            i.draw()
            
ShellEffect()