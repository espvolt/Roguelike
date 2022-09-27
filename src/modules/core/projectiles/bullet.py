from html import entities
from ... import projectile
import math
import pygame
from ... import util
from ... import globals as gb
from ... import map
from ... import object
from ... import sound

class Bullet(projectile.Projectile):
    sounds: list[pygame.mixer.Sound] = []
    
    def __init__(self, x: float, y: float, angle: float, velocity: float, color: tuple[int, int, int], doSound: bool=False):
        super(Bullet, self).__init__()
        self.doSound = doSound

        if (self.doSound):
            self.sound = pygame.mixer.Sound(gb.baseDir + "/modules/core/assets/weapons/BulletFlyBySound.wav")


        self.x = x
        self.y = y

        self.angle = angle
        self.velocity = velocity

        self.points = []
        self.color = color

        for _ in range(5):
            new = []
            new.append(x)
            new.append(y)
            self.points.append(new)

        self.lifetime = 0

        self.inRangeOfPlayer = False
        self.distanceThreshold = 250

        self.shouldPlay = False

    def killBullet(self):
        gb.projectiles.pop(self.id)

    def update(self):
        for i in range(len(self.points) - 1, -1, -1):
            if (i != 0):
                self.points[i][0] = self.points[i - 1][0]
                self.points[i][1] = self.points[i - 1][1]

            else:
                self.points[0][0] = self.x
                self.points[0][1] = self.y

        textX = self.x
        textY = self.y
        
        l = object.Line(self.x, self.y, self.x + math.cos(self.angle) * self.velocity, self.y + math.sin(self.angle) * self.velocity)
        
        for i in list(gb.entities.values()):
            if (i.hitbox.intersects(l)):
                i.damage(1, self.angle)
                self.killBullet()
                return

        for i in range(5):
            nextX = textX + math.cos(self.angle) * self.velocity / 5
            nextY = textY + math.sin(self.angle) * self.velocity / 5

            l = object.Line(nextX, nextY, textX, textY)

            neighbors = map.getNeighbors(textX // 32, textY // 32)
            neighbors[(0, 0)] = map.getObject(textX // 32, textY // 32)
            for i in neighbors:
                obj = neighbors[i]

                if (obj is None):
                    continue

                for i in obj.collisionLines:
                    if (l.intersects(i)):
                        self.killBullet()

                        return
            textX += math.cos(self.angle) * self.velocity / 5
            textY += math.sin(self.angle) * self.velocity / 5
        
        
                
        self.x += math.cos(self.angle) * self.velocity
        self.y += math.sin(self.angle) * self.velocity

        self.lifetime += 1

        self.distToPlayer = math.sqrt((self.x - gb.playerEntity.x) ** 2 + (self.y - gb.playerEntity.y) ** 2)

        if (self.doSound):
            if (self.shouldPlay):
                
                sound.playSoundPos((self.x, self.y), (gb.playerEntity.x, gb.playerEntity.y), 1, self.sound)

            if (self.distToPlayer < self.distanceThreshold):
                self.shouldPlay = True
            else:
                self.shouldPlay = False

        if (self.lifetime > 50):
            self.killBullet()

    def draw(self):
        rect = pygame.Surface((1, 1))
        rect.set_colorkey((0, 0, 0))
        rect.fill(self.color)

        util.blitRotate(gb.display, rect, (self.x, self.y), (.5, 0), self.angle * 180 / math.pi)
        
        prev = (self.x, self.y)

        for i in self.points:
            dx = i[0] - prev[0]
            dy = i[1] - prev[1]

            dist = math.sqrt(dx ** 2 + dy ** 2)
            rect = pygame.Surface((dist, 1))
            rect.set_colorkey((0, 0, 0))
            rect.fill(self.color)

            util.blitRotate(gb.display, rect, (i[0], i[1]), (.5, 0), (self.angle * 180 / -math.pi))
            prev = i