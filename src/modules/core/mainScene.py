from .. import globals as gb
from .. import scene
from .. import map
from .objects import basicObjects
from .floors import basicFloors
from .. import object
from .entities import basicHuman
from .entities.weapons import init
from .projectiles.bullet import Bullet
from .. import sound
import math
from .. import floor

from .. import util
from .. import sound

import pygame
import copy

class MainScene(scene.Scene):
    def __init__(self):
        gb.playerEntity = basicHuman.HumanPlayer(0, 0, copy.deepcopy(gb.CharacterData["MC"]))
        basicHuman.BasicHuman(20, 20, "B", copy.deepcopy(gb.CharacterData["MC"]))
        super(MainScene, self).__init__("core:Main")


        map.addObject(basicObjects.WoodenObject(1, 1))
        map.addObject(basicObjects.WoodenObject(3, 2))
        map.addObject(basicObjects.WoodenObject(3, 3))
        map.addObject(basicObjects.WoodenObject(3, 4))
        map.addObject(basicObjects.WoodenObject(3, 5))
        map.addObject(basicObjects.WoodenObject(4, 5))
        map.addObject(basicObjects.WoodenObject(4, 6))

        map.addObject(basicObjects.WoodenObject(1, 2))
        map.addObject(basicObjects.WoodenObject(2, 2))
        map.addObject(basicObjects.WoodenObject(2, 3))

        map.addObject(basicObjects.WoodenObject(5, 1))
        map.addObject(basicObjects.WoodenObject(4, 2))
        map.addObject(basicObjects.WoodenObject(5, 2))
        map.addObject(basicObjects.WoodenObject(4, 3))

        map.addObject(basicObjects.WoodenObject(7, 1))
        map.addObject(basicObjects.WoodenObject(8, 2))

        map.addObject(basicObjects.WoodenObject(7, 2))
        map.addObject(basicObjects.WoodenObject(7, 3))

        object.Object.updateAllVisionLines()
        object.Object.updateAllCollisionLines()

        for i in range(30):
            for j in range(30):
                if ((i, j) not in gb.tileMap):
                    gb.floors[(i, j)] = basicFloors.WoodenFloor()
       
    def update(self):
        map.updateMap()

        sound.update()

        for i in gb.effects:
            gb.effects[i].update()
        
        for i in list(gb.entities.values()):
            i.update()

        for i in list(gb.bodyentities.values()):
            i.update()

        for i in list(gb.projectiles.values()):
            i.update()


    def draw(self):
        map.drawMap()

        for i in gb.floors:
            gb.floors[i].draw(i[0], i[1])

        for i in gb.effects:
            gb.effects[i].backGroundDraw()

        for i in list(gb.bodyentities.values()):
            i.draw()
            
        for i in list(gb.entities.values()):
            i.draw()

        for i in list(gb.projectiles.values()):
            i.draw()

        for i in gb.effects:
            gb.effects[i].foreGroundDraw()



        
        

def setup():
    global soundData
    gb.currentScene = MainScene()
    sound.playMusic(gb.baseDir + "/modules/core/assets/DeepBlue.wav", .3)
    

    # gb.player.pregenerateSong(gb.baseDir + "/modules/core/assets/db.mp3", 1, gb.baseDir + "/modules/core/temp/songdata", False)
    # gb.player.playsoundbackgroundedit("db.mp3", soundData, start = 60)


    
    