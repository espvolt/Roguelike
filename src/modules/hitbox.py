import math
import numpy as np

from . import globals as gb
from . import util
from . import object

import pygame


class Hitbox:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.ally = False
        self.active = False
        ...

    def contains(self, x: float, y: float) -> bool:
        return False

    def hits(self, other: "Hitbox") -> bool:
        return False

    def intersects(self, line: object.Line) -> bool:
        return False

    def draw(self):
        return

class Circle(Hitbox):
    def __init__(self, x, y, radius: float):
        super(Circle, self).__init__(x, y)
        self.radius = radius
        

    def contains(self, x: float, y: float) -> bool:
        return (x - self.x) ** 2 + (y - self.y) ** 2 <= self.radius ** 2

    
    def intersects(self, line: object.Line) -> bool:
        e = np.array(line.point)
        l = np.array(line.point_)

        c = np.array((self.x, self.y))

        d = np.array([l[0] - e[0], l[1] - e[1]])
        f = np.array([e[0] - c[0], e[1] - c[1]])

        a = d.dot(d)
        b = 2 * f.dot(d)
        c = f.dot(f) - self.radius ** 2

        discriminant = b ** 2 - 4 * a * c

        if (discriminant < 0):
            return False

        else:
            discriminant = math.sqrt(discriminant)

            t1 = (-b - discriminant) / (2 * a)
            t2 = (-b + discriminant) / (2 * a)

            if ((t1 >= 0 and t1 <= 1) or (t1 >= 0 and t2 <= 1)):
                return True

        return False

    def draw(self, color: tuple[int, int, int]):
        pygame.draw.circle(gb.display, color, (self.x, self.y), self.radius)\

    

class Rectangle(Hitbox):
    def __init__(self, x, y, w: float, h: float, originX: float=0, originY: float=0, angle: float=0):
        super(Rectangle, self).__init__(x, y)

        self.w = w
        self.h = h
        self.origin = [originX, originY]
        self.angle = angle

    def contains(self, x: float, y: float):
        a = Rectangle.rotatePoint(self.origin, self.x, self.y, self.angle)
        b = Rectangle.rotatePoint(self.origin, self.x + self.w, self.y, self.angle)
        c = Rectangle.rotatePoint(self.origin, self.x, self.y + self.h, self.angle)
        d = Rectangle.rotatePoint(self.origin, self.x + self.w, self.y + self.h, self.angle)

        p = (x, y)
        a_ = Rectangle.calculateArea(a, p, d)
        b_ = Rectangle.calculateArea(d, p, c)
        c_ = Rectangle.calculateArea(c, p, b)
        d_ = Rectangle.calculateArea(p, b, a)

        return sum(a_, b_, c_, d_) <= self.w * self.h

    def intersects(self, line: object.Line) -> bool:
        a = Rectangle.rotatePoint(self.origin, self.x, self.y, self.angle)
        b = Rectangle.rotatePoint(self.origin, self.x + self.w, self.y, self.angle)
        c = Rectangle.rotatePoint(self.origin, self.x, self.y + self.h, self.angle)
        d = Rectangle.rotatePoint(self.origin, self.x + self.w, self.y + self.h, self.angle)

        a_ = object.Line(a[0], b[0], a[1], b[1])
        b_ = object.Line(a[0], c[0], a[1], c[1])
        c_ = object.Line(c[0], d[0], c[1], d[1])
        d_ = object.Line(b[0], d[0], b[1], d[1])

        return a_.intersects(line) or b_.intersects(line) or c_.intersects(line) or d_.intersects(line)

        ...

    @staticmethod 
    def calculateArea(a, b, c) -> float:
        return abs((b[0] * a[1] - a[0] * b[1]) + (c[0] * b[1] - b[0] * c[1]) + (a[0] * c[1] - c[0] * a[1])) / 2

    @staticmethod 
    def rotatePoint(origin, x, y, angle):
        ox, oy = origin
    
        qx = ox + math.cos(angle) * (x - ox) - math.sin(angle) * (y - oy)
        qy = oy + math.sin(angle) * (x - ox) + math.cos(angle) * (y - oy)

        return qx, qy

    def setAngle(self, new):
        self.angle = new

    def draw(self, color: tuple[int, int, int]):
        surf = pygame.Surface((self.w, self.h))
        surf.set_colorkey([0, 0, 0])
        surf.fill(color)

        util.blitRotate(gb.display, surf, (self.x, self.y), self.origin, self.angle * 180 / math.pi)
