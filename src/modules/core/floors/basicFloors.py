import random
from ... import floor
import pygame
from ... import globals as gb
from ... import sound
from ... import entity
from ... import util

class WoodenFloor(floor.Floor):
    image = pygame.image.load(gb.baseDir + "/modules/core/assets/floors/WoodFloor/WoodFloor.png")

    def playSound(self, x: float, y: float, steppedOn: entity.Entity):
        s = steppedOn.sounds.get("WoodStep")
        if (s == None):
            return

        if (steppedOn.walking):
            sound.playSoundPos((gb.playerEntity.x, gb.playerEntity.y), (steppedOn.x, steppedOn.y), .5, random.choice(s))
        else:
            sound.playSoundPos((gb.playerEntity.x, gb.playerEntity.y), (steppedOn.x, steppedOn.y), 1, random.choice(s))

    def draw(self, x: float, y: float):
        util.blitCamera(gb.display, WoodenFloor.image, (x * 32, y * 32))