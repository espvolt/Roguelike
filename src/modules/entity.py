import sys
import os

from . import hitbox
from . import globals as gb
from . import animation as anim
import json
import pygame
 
def loadCharacterData(*paths):
    for path in paths:
        for i in os.listdir(path):
            if (i.startswith("__")):
                continue
            currentFile = path + "/" + i

            if (os.path.isdir(currentFile)):
                data = None
                with open(currentFile + "/data.json", "r") as f:
                    data = json.load(f)

                gb.CharacterData[i] = {}
                for animation in data:
                    if (animation.startswith("_")):
                        gb.CharacterData[i][animation] = data[animation]
                        continue
                    src: str = data[animation]["src"]

                    cacheName = i + ":" + animation
                    data[animation]["componentKey"] = animation
                    if (src.endswith(".gif")):
                        gb.CharacterData[i][animation] = AnimationComponent(anim.Animation.fromGif(gb.baseDir + "/" + src, cacheName), data[animation]["offset"], data[animation])
                    elif (src.endswith(".png")):
                        gb.CharacterData[i][animation] = AnimationComponent(anim.Animation.image(gb.baseDir + "/" + src, cacheName), data[animation]["offset"], data[animation])

                    gb.CharacterData[i][animation].animation.loops = True if "loops" not in data[animation] else data[animation]["loops"]
                    gb.CharacterData[i][animation].animation.frameStep = 0 if "frameStep" not in data[animation] else data[animation]["frameStep"]




class AnimationComponent:
    def __init__(self, animation: anim.Animation, offset: tuple[float, float], data: dict):
        self.animation = animation
        self.offset = offset
        self.data = data

class Entity:
    idCount = -sys.maxsize
    def __init__(self, x: float, y: float, name: str, dead=False):
        self.x = x
        self.y = y
        self.xVelocity = 0
        self.yVelocity = 0
        self.name = name
        self.speed = 0
        self.angle = 0
        self.lookAngle = 0
        self.id = Entity.idCount
        self.hitbox: hitbox.Hitbox = None  
        self.walking = False

        self.sounds: dict[str, list[pygame.mixer.Sound]] = {}

        if (not dead):
            gb.entities[self.id] = self
        else:
            gb.bodyentities[self.id] = self
        Entity.idCount += 1

    def update(self):
        ...

    def draw(self):
        ...

    def damage(self, x: float, angle: float, kill: float=False):
        ...

    