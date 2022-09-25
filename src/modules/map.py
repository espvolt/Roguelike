import math
from tkinter import E
from . import globals as gb
from . import object
import pygame

def addObject(obj: object.Object):
    obj.active = True
    gb.tileMap[(obj.x, obj.y)] = obj

def removeObject(x: int, y: int) -> object.Object:
    return gb.tileMap.pop((x, y))
    

def getObject(x: int, y: int) -> object.Object | None:
    if ((x, y) in gb.tileMap):
        return gb.tileMap[(x, y)]
    else:
        return None    

def updateMap():
    for k in gb.tileMap:
        gb.tileMap[k].update()

def drawMap():
    for k in gb.tileMap:
        gb.tileMap[k].draw()

def drawVisionLines(color: tuple[float, float, float] | list[float]):
    for k in gb.tileMap:
        gb.tileMap[k].drawVisionLines(color)

def drawCollisionLines(color: tuple[float, float, float] | list[float]):
    for k in gb.tileMap:
        gb.tileMap[k].drawCollisionLines(color)

class Node: 
    def __init__(self, x: float, y: float, f: float, g: float, h: float, parent: "Node"):
        self.x = x
        self.y = y
        self.f = f
        self.g = g
        self.h = h
        self.parent = parent


    def __gt__(self, other: "Node"):
        return self.f > other.f

    def __lt__(self, other:"Node"):
        return self.f < other.f
    
    def __ge__(self, other: "Node"):
        return self.f >= other.f

    def __le__(self, other: "Node"):
        return self.f <= other.f

    def __eq__(self, other: "Node"):
        return self.f == other.f and self.x == other.x and self.y == other.y

    def __str__(self):
        return str(self.x) + " " + str(self.y) + " " + str(self.f)

    def __repr__(self):
        return self.__str__()

    ...

def drawPath(path: list[Node], color: list[float] | tuple[float, float, float]):
    for i in path:
        pygame.draw.rect(gb.display, color, pygame.Rect(i.x * 32, i.y * 32, 32, 32))

def findPath(x: int, y: int, x_: int, y_: int):
    openl = [Node(x, y, 0, 0, 0, None)]
    closedl = []

    while (len(openl) != 0):  

        q = openl.pop(0)

        neighbors = getNeighbors(q.x, q.y, eight=True)

        for i in neighbors:
            obj = neighbors[i]

            
            if (obj is not None and obj.flags["SOLID"]):
                continue
            node = Node(q.x + i[0], q.y + i[1], 0, 0, 0, q)

            if (q.x + i[0] == x_ and q.y + i[1] == y_):
                res = []

                while(node.parent is not None):
                    res.append(node)
                    node = node.parent

                res.append(node)

                return res[::-1]


            node.g = q.g + 1

            dx = abs(node.x - x_)
            dy = abs(node.y - y_)

            node.h = dx + dy
            node.f = node.g + node.h

            skip = False

            for i in openl:
                if (i.x == node.x and i.y == node.y and node.f > i.f):
                    skip = True
                    break

            if (skip):
                continue

            skip = False

            for i in closedl:
                if (i.x == node.x and i.y == node.y and node.f > i.f):
                    skip = True
                    break

            if (skip):
                continue

            openl.append(node)

        closedl.append(q)
        openl.sort()

    return closedl    

            
            


normalIndexes = [(0, 1),
                     (1, 0),
                     (-1, 0),
                     (0, -1)]

eightIndexes = [(0, 1),
                (1, 0),
                (-1, 0),
                (0, -1),
                (1, 1),
                (-1, -1),
                (1, -1),
                (-1, 1)]


def getNeighbors(x: int, y: int, eight: bool=False) -> dict[tuple[int, int], object.Object | None]:
    
    res = {}

    arr = eightIndexes if eight else normalIndexes

    for i in arr:
        res[i] = getObject(x + i[0], y + i[1])

    return res


def doCollision(x: float, y: float, vx: float, vy: float, radius: float) -> list[float, float, bool]:
    neighbors = getNeighbors(x // 32, y // 32, eight=8)

    col = False

    for j in neighbors: # ADAM I LOVE YOU
        obj = neighbors[j]
        
        if (obj is None):
            continue
        
        for j in obj.collisionLines:
            a_to_b = (j.point_[0] - j.point[0], j.point_[1] - j.point[1])
            perpendicular = [-a_to_b[1], a_to_b[0]]
        
            d = math.sqrt(perpendicular[0] ** 2 + perpendicular[1] ** 2)

            nx = perpendicular[0] / d
            ny = perpendicular[1] / d

            tx = x - (j.point[0] + j.point_[0]) / 2
            ty = y - (j.point[1] + j.point_[1]) / 2

            pdot = nx * tx + ny * ty

            if (pdot > 0):
                nx *= -1
                ny *= -1
            
            
            ndot = nx * -vx + ny * -vy

            onside = j.onSide(x + nx * radius, y + ny * radius)

            if (ndot <= 0 and ((onside != j.onSide(x + nx * radius + vx,
                y + ny * radius + vy) and j.isPointOver(x + nx * radius, y + ny * radius)) or j.distFrom(x, y) < radius)):
                vx += nx * ndot
                vy += ny * ndot
                col = True


    return vx, vy, col      


    