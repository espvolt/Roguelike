import math
from turtle import width
import pygame

from ... import globals as gb
from ... import object
from ... import map
from ... import util

class BasicObject(object.Object):
    wallWidth = 0
    def __init__(self, x: int, y: int):
        super(BasicObject, self).__init__(x, y)
        
        self.flags["FULL_TILE_OBJ"] = True
        self.flags["SOLID"] = True

    def updateCollisionLines(self):
        self.collisionLines.clear()

        neighbors = map.getNeighbors(self.x, self.y)

        up = neighbors[(0, -1)] is None or not neighbors[(0, -1)].flags["FULL_TILE_OBJ"]
        do = neighbors[(0, 1)] is None or not neighbors[(0, 1)].flags["FULL_TILE_OBJ"]
        ri = neighbors[(1, 0)] is None or not neighbors[(1, 0)].flags["FULL_TILE_OBJ"]
        le = neighbors[(-1, 0)] is None or not neighbors[(-1, 0)].flags["FULL_TILE_OBJ"]
        

        if (up):
            self.collisionLines.append(object.Line(self.x * 32, self.y * 32, self.x * 32 + 32, self.y * 32))

        if (do):
            self.collisionLines.append(object.Line(self.x * 32, self.y * 32 + 32, self.x * 32 + 32, self.y * 32 + 32))

        if (ri):
            self.collisionLines.append(object.Line(self.x * 32 + 32, self.y * 32, self.x * 32 + 32, self.y * 32 + 32))

        if (le):
            self.collisionLines.append(object.Line(self.x * 32, self.y * 32, self.x * 32, self.y * 32 + 32))




    def updateVisionLines(self):
        self.visionLines.clear()

        neighbors = map.getNeighbors(self.x, self.y, True)
        up = neighbors[(0, -1)] is None or not neighbors[(0, -1)].flags["FULL_TILE_OBJ"]
        do = neighbors[(0, 1)] is None or not neighbors[(0, 1)].flags["FULL_TILE_OBJ"]
        ri = neighbors[(1, 0)] is None or not neighbors[(1, 0)].flags["FULL_TILE_OBJ"]
        le = neighbors[(-1, 0)] is None or not neighbors[(-1, 0)].flags["FULL_TILE_OBJ"]
        dur = neighbors[(1, -1)] is None or not neighbors[(1, -1)].flags["FULL_TILE_OBJ"]
        dul = neighbors[(-1, -1)] is None or not neighbors[(-1, -1)].flags["FULL_TILE_OBJ"]
        ddl = neighbors[(-1, 1)] is None or not neighbors[(-1, 1)].flags["FULL_TILE_OBJ"]
        ddr = neighbors[(1, 1)] is None or not neighbors[(1, 1)].flags["FULL_TILE_OBJ"]

        x, y = self.getDrawPosition()

        if (up):
            match (ri + le * 2):
                case (3):
                    self.visionLines.append(object.Line(x + self.wallWidth, y + self.wallWidth, x + 32 - self.wallWidth, y + self.wallWidth))
                case (0):
                    self.visionLines.append(object.Line(x, y + self.wallWidth, x + 32, y + self.wallWidth))
                case (2):
                    self.visionLines.append(object.Line(x + self.wallWidth, y + self.wallWidth, x + 32, y + self.wallWidth))
                case (1):
                    self.visionLines.append(object.Line(x, y + self.wallWidth, x + 32 - self.wallWidth, y + self.wallWidth))


        
        if (do):
            match (le + ri * 2):
                case (3):
                    self.visionLines.append(object.Line(x + self.wallWidth, y + 32 - self.wallWidth, x + 32 - self.wallWidth, y + 32 - self.wallWidth))
                case (0):
                    self.visionLines.append(object.Line(x, y + 32 - self.wallWidth, x + 32, y + 32 - self.wallWidth))
                case (2):
                    self.visionLines.append(object.Line(x, y + 32 - self.wallWidth, x + 32 - self.wallWidth, y + 32 - self.wallWidth))
                case (1):
                    self.visionLines.append(object.Line(x + self.wallWidth, y + 32 - self.wallWidth, x + 32, y + 32 - self.wallWidth))



        if (ri):
            match (do + up * 2):
                case (3):
                    self.visionLines.append(object.Line(x + 32 - self.wallWidth, y + self.wallWidth, x + 32 - self.wallWidth, y + 32 - self.wallWidth))
                case (0):
                    self.visionLines.append(object.Line(x + 32 - self.wallWidth, y, x + 32 - self.wallWidth, y + 32))
                case (2):
                    self.visionLines.append(object.Line(x + 32 - self.wallWidth, y + self.wallWidth, x + 32 - self.wallWidth, y + 32))
                case (1):
                    self.visionLines.append(object.Line(x + 32 - self.wallWidth, y, x + 32 - self.wallWidth, y + 32 - self.wallWidth))
        

        if (le):
            match (up + do * 2):
                case (3):
                    self.visionLines.append(object.Line(x + self.wallWidth, y + self.wallWidth, x + self.wallWidth, y + 32 - self.wallWidth))
                case (0):
                    self.visionLines.append(object.Line(x + self.wallWidth, y, x + self.wallWidth, y + 32))

                case (2):
                    self.visionLines.append(object.Line(x + self.wallWidth, y, x + self.wallWidth, y + 32 - self.wallWidth))
                case (1):
                    self.visionLines.append(object.Line(x + self.wallWidth, y + self.wallWidth, x + self.wallWidth, y + 32))
        
        if (not ri and dur and not up):
            self.visionLines.append(object.Line(x + 32 - self.wallWidth, y, x + 32 - self.wallWidth, y + self.wallWidth))
            self.visionLines.append(object.Line(x + 32 - self.wallWidth, y + self.wallWidth, x + 32, y + self.wallWidth))


        if (not le and ddl and not do):
            self.visionLines.append(object.Line(x, y + 32 - self.wallWidth, x + self.wallWidth, y + 32 - self.wallWidth))
            self.visionLines.append(object.Line(x + self.wallWidth, y + 32 - self.wallWidth, x + self.wallWidth, y + 32 + self.wallWidth))

        if (not le and dul and not up):
            self.visionLines.append(object.Line(x, y + self.wallWidth, x + self.wallWidth, y + self.wallWidth))
            self.visionLines.append(object.Line(x + self.wallWidth, y, x + self.wallWidth, y + self.wallWidth))



        if (not ri and ddr and not do):
            self.visionLines.append(object.Line(x + 32 - self.wallWidth, y + 32 - self.wallWidth, x + 32, y + 32 - self.wallWidth))
            self.visionLines.append(object.Line(x + 32 - self.wallWidth, y + 32 - self.wallWidth, x + 32 - self.wallWidth, y + 32))


        ...
    def draw(self):
        if (not self.active):
            return

        neighbors = map.getNeighbors(self.x, self.y, True)
        up = neighbors[(0, -1)] is None or not neighbors[(0, -1)].flags["FULL_TILE_OBJ"]
        do = neighbors[(0, 1)] is None or not neighbors[(0, 1)].flags["FULL_TILE_OBJ"]
        ri = neighbors[(1, 0)] is None or not neighbors[(1, 0)].flags["FULL_TILE_OBJ"]
        le = neighbors[(-1, 0)] is None or not neighbors[(-1, 0)].flags["FULL_TILE_OBJ"]
        dur = neighbors[(1, -1)] is None or not neighbors[(1, -1)].flags["FULL_TILE_OBJ"]
        dul = neighbors[(-1, -1)] is None or not neighbors[(-1, -1)].flags["FULL_TILE_OBJ"]
        ddl = neighbors[(-1, 1)] is None or not neighbors[(-1, 1)].flags["FULL_TILE_OBJ"]
        ddr = neighbors[(1, 1)] is None or not neighbors[(1, 1)].flags["FULL_TILE_OBJ"]

        if (up):
            match (ri + le * 2):
                case (3):
                    util.blitCamera(gb.display, pygame.transform.rotate(self.alone, 180), self.getDrawPosition())
                case (0):
                    util.blitCamera(gb.display, pygame.transform.rotate(self.all, 180), self.getDrawPosition())
                case (2):
                    util.blitCamera(gb.display, pygame.transform.rotate(self.left, 180), self.getDrawPosition())
                case (1):
                    util.blitCamera(gb.display, pygame.transform.rotate(self.right, 180), self.getDrawPosition())

        
        if (do):
            match (le + ri * 2):
                case (3):
                    util.blitCamera(gb.display, self.alone, self.getDrawPosition())
                case (0):
                    util.blitCamera(gb.display, self.all, self.getDrawPosition())
                case (2):
                    util.blitCamera(gb.display, self.left, self.getDrawPosition())
                case (1):
                    util.blitCamera(gb.display, self.right, self.getDrawPosition())


        if (ri):
            match (do + up * 2):
                case (3):
                    util.blitCamera(gb.display, pygame.transform.rotate(self.alone, 90), self.getDrawPosition())
                case (0):
                    util.blitCamera(gb.display, pygame.transform.rotate(self.all, 90), self.getDrawPosition())
                case (2):
                    util.blitCamera(gb.display, pygame.transform.rotate(self.left, 90), self.getDrawPosition())
                case (1):
                    util.blitCamera(gb.display, pygame.transform.rotate(self.right, 90), self.getDrawPosition())
        

        if (le):
            match (up + do * 2):
                case (3):
                    util.blitCamera(gb.display, pygame.transform.rotate(self.alone, 270), self.getDrawPosition())
                case (0):
                    util.blitCamera(gb.display, pygame.transform.rotate(self.all, 270), self.getDrawPosition())
                case (2):
                    util.blitCamera(gb.display, pygame.transform.rotate(self.left, 270), self.getDrawPosition())
                case (1):
                    util.blitCamera(gb.display, pygame.transform.rotate(self.right, 270), self.getDrawPosition())
        
        if (not ri and dur and not up):
            topCornerPiece = neighbors[(0, -1)].cornerRevLeft
            rightCornerPiece = neighbors[(1, 0)].cornerLeft

            util.blitCamera(gb.display, pygame.transform.rotate(topCornerPiece, 180), self.getDrawPosition())
            util.blitCamera(gb.display, pygame.transform.rotate(rightCornerPiece, 180), self.getDrawPosition())

        if (not le and ddl and not do):
            bottomCornerPiece = neighbors[(0, 1)].cornerRevLeft
            rightCornerPiece = neighbors[(-1, 0)].cornerLeft

            util.blitCamera(gb.display, rightCornerPiece, self.getDrawPosition())
            util.blitCamera(gb.display, bottomCornerPiece, self.getDrawPosition())

        if (not le and dul and not up):
            leftCornerPiece = neighbors[(-1, 0)].cornerRight
            topCornerPiece = neighbors[(0, -1)].cornerRevRight

            util.blitCamera(gb.display, pygame.transform.rotate(leftCornerPiece, 180), self.getDrawPosition())
            util.blitCamera(gb.display, pygame.transform.rotate(topCornerPiece, 180), self.getDrawPosition())

        if (not ri and ddr and not do):
            bottomCornerPiece = neighbors[(0, 1)].cornerRevRight
            rightCornerPiece = neighbors[(1, 0)].cornerRight

            util.blitCamera(gb.display, rightCornerPiece, self.getDrawPosition())
            util.blitCamera(gb.display, bottomCornerPiece, self.getDrawPosition())
            
    
class WoodenObject(BasicObject):
    alone = pygame.image.load(gb.baseDir + "/modules/core/assets/objects/WoodenObject/WoodenObject.png")
    left = pygame.image.load(gb.baseDir + "/modules/core/assets/objects/WoodenObject/WoodenConnectorLeft.png")
    right = pygame.image.load(gb.baseDir + "/modules/core/assets/objects/WoodenObject/WoodenConnectorRight.png")
    all = pygame.image.load(gb.baseDir + "/modules/core/assets/objects/WoodenObject/WoodenConnectorAll.png")
    cornerLeft = pygame.image.load(gb.baseDir + "/modules/core/assets/objects/WoodenObject/WoodenCornerLeft.png")
    cornerRight = pygame.image.load(gb.baseDir + "/modules/core/assets/objects/WoodenObject/WoodenCornerRight.png")
    cornerRevRight = pygame.image.load(gb.baseDir + "/modules/core/assets/objects/WoodenObject/WoodenCornerRevRight.png")
    cornerRevLeft = pygame.image.load(gb.baseDir + "/modules/core/assets/objects/WoodenObject/WoodenCornerRevLeft.png")

    wallWidth = 6
    def __init__(self, x: int, y: int):
        super(WoodenObject, self).__init__(x, y)

    def update(self):
        ...
    




        

            
        
        

