import pygame
import math
from . import globals as gb

def onSegment(p, q, r):
    if ( (q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and 
           (q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1]))):
        return True
    return False
  
def orientation(p, q, r):
    val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1]))
    if (val > 0):
          
        return 1
    elif (val < 0):
          
        return 2
    else:
          
        return 0

def doIntersect(p1,q1,p2,q2):
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)
  
    if ((o1 != o2) and (o3 != o4)):
        return True
  
    if ((o1 == 0) and onSegment(p1, p2, q1)):
        return True
  
    if ((o2 == 0) and onSegment(p1, q2, q1)):
        return True
  
    if ((o3 == 0) and onSegment(p2, p1, q2)):
        return True
  
    if ((o4 == 0) and onSegment(p2, q1, q2)):
        return True
  
    return False

class Line:
    def __init__(self, x, y, x_, y_):
        self.point = [x, y]
        self.point_ = [x_, y_]

    def intersects(self, other: "Line"):
        return doIntersect(self.point, self.point_, other.point, other.point_)
    
    def closestPoint(self, point: tuple[float, float]):
        a_to_b = [self.point_[0] - self.point[0], self.point_[1] - self.point[1]]
        
        perpendicular = [-a_to_b[1], a_to_b[0]]

        Q = [point[0] + perpendicular[0], point[1] + perpendicular[0]]

        x = ((self.point[0]*self.point_[1] - self.point[1]*self.point_[0])
            *(point[0] - Q[0]) - (self.point[0]-self.point_[0])*(point[0]*Q[1] - point[1]*Q[0]))/((self.point[0] - self.point_[0])
            *(point[1]-Q[1]) - (self.point[1] - self.point_[1])*(point[1]-Q[1])),
        y = ((self.point[0]*self.point_[1] - self.point[1]*self.point_[0])
            *(point[1] - Q[1]) - (self.point[1]-self.point_[1])
            *(point[0]*Q[1] - point[1]*Q[0]))/((self.point[0] - self.point_[0])
            *(point[1]-Q[1]) - (self.point[1] - self.point_[1])*(point[1]-Q[1])) 
        
        return [x, y]

    def onSide(self, x: float, y: float):
        if (self.point[0] == self.point_[0]):
            return x < self.point[0]
        else:
            return y > (x - self.point[0]) * (self.point_[1] - self.point[1]) / (self.point_[0] - self.point[0]) + self.point[1]

    def isPointOver(self, x: float, y: float) -> bool:
        res = None

        if (self.point[0] == self.point_[0]):
            t = (y - self.point[1]) / (self.point_[1] - self.point[1])

        else:
            t = (x - self.point[0]) / (self.point_[0] - self.point[0])

        return t > 0 and t < 1

    def distFrom(self, x, y):
        if(self.isPointOver(x, y)):
            A = x - self.point[0]
            B = y - self.point[1]
            C = self.point_[0] - self.point[0]
            D = self.point_[1] - self.point[1]

            dot = A * -D + B * C
            len_sq = D * D + C * C

            return abs(dot) / math.sqrt(len_sq)
        else:
            distS1 = (self.point[0] - x) * (self.point[0] - x) + (self.point[1] - y) * (self.point[1] - y)
            distS2 = (self.point_[0] - x) * (self.point_[0] - x) + (self.point_[1] - y) * (self.point_[1] - y)
            return math.sqrt(min(distS1, distS2))

            
class Object:
    def __init__(self, x: int, y: int):
        self.active = False
        self.x = x
        self.y = y
        self.visionLines: list[Line] = []
        self.collisionLines: list[Line] = []
        
        self.flags: dict = {}

    def update(self):
        ...

    def draw(self):
        ...

    def setPosition(self, x, y) -> "Object":
        res = None


        if ((x,  y) in gb.tileMap):
            res = gb.tileMap[(x, y)]

        if (self.x, self.y) in gb.tileMap:
            gb.tileMap.pop(self.x, self.y)

        self.x = x
        self.y = y

        gb.tileMap[(x, y)] = self

        Object.updateAllVisionLines()
        Object.updateAllCollisionLines()

        return res

    @staticmethod
    def updateAllVisionLines():
        for i in gb.tileMap:
            gb.tileMap[i].updateVisionLines()
        ...

    @staticmethod
    def updateAllCollisionLines():
        for i in gb.tileMap:
            gb.tileMap[i].updateCollisionLines()
        ...

    def updateVisionLines(self):
        pass

    def updateCollisionLines(self):
        pass

    def getDrawPosition(self):
        return [self.x * 32, self.y * 32]

    def drawVisionLines(self, color: tuple[float, float, float] | list[float]):
        for i in self.visionLines:
            pygame.draw.line(gb.display, color, i.point, i.point_, 2)

    def drawCollisionLines(self, color: tuple[float, float, float] | list[float]):
        for i in self.collisionLines:
            pygame.draw.line(gb.display, color, i.point, i.point_, 2)
            
    def getCollisionLines(self) -> list[Line]:
        return []

   

