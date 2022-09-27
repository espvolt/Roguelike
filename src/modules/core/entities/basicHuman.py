from pyexpat.errors import XML_ERROR_INVALID_TOKEN

from ..floors import basicFloors
from ... import entity
from ... import animation as anim
from ... import globals as gb
from ... import util
from . import weapon
from ... import hitbox
from ... import util
from ... import map
from ... import object
from ... import entity
from ..effects import blood

import numpy as np

import math
import pygame

weapons = [None, "spistol"]

class Body(entity.Entity):
    def __init__(self, x: float, y: float, animation: entity.AnimationComponent, side: entity.AnimationComponent, carry: entity.AnimationComponent, angle: float, vAngle: float, kill: bool=True):
        super(Body, self).__init__(x, y, "", dead=True)
        self.angle = angle
        self.vAngle = vAngle
        self.velocity = 10
        self.animation = animation
        self.side = side
        self.collided = False
        self.kill = kill
        self.carry = carry
        self.bloodEffect = None        
        self.vMul = .8
        self.done = False
        self.bloodSpawned = False
        self.drawAnim = self.animation

    def update(self):
        if (self.done):
            self.animation.animation.updateAnimation()
            return
        self.xVelocity = math.cos(self.vAngle) * self.velocity
        self.yVelocity = math.sin(self.vAngle) * self.velocity

        neighbors = map.getNeighbors(self.x // 32, self.y // 32, eight=8)

        fin = False

        for i in neighbors: # ADAM I LOVE YOU
            obj = neighbors[i]
            
            if (obj is None):
                continue
            
            for j in obj.collisionLines:
                a_to_b = (j.point_[0] - j.point[0], j.point_[1] - j.point[1])
                perpendicular = [-a_to_b[1], a_to_b[0]]
            
                d = math.sqrt(perpendicular[0] ** 2 + perpendicular[1] ** 2)

                nx = perpendicular[0] / d
                ny = perpendicular[1] / d

                tx = self.x - (j.point[0] + j.point_[0]) / 2
                ty = self.y - (j.point[1] + j.point_[1]) / 2

                pdot = nx * tx + ny * ty

                if (pdot > 0):
                    nx *= -1
                    ny *= -1
                
                r = 1
                ndot = nx * -self.xVelocity + ny * -self.yVelocity

                onside = j.onSide(self.x + nx * r, self.y + ny * r)
    
                if (ndot <= 0 and ((onside != j.onSide(self.x + nx * r + self.xVelocity,
                    self.y + ny * r + self.yVelocity) and j.isPointOver(self.x + nx * r, self.y + ny * r)) or j.distFrom(self.x, self.y) < r)):
                    self.xVelocity += nx * ndot
                    self.yVelocity += ny * ndot
                    self.angle = -math.atan2(nx * ndot, ny * ndot) - math.pi / 2
                    self.drawAnim = self.side
                    self.collided = True
                    self.velocity = 0
                    print(":)")

                    fin = True
                    break
            
            if (fin):
                break
        
        if (abs(self.velocity) < .17):
            if (not self.collided and self.kill and not self.bloodSpawned):
                self.bloodEffect = blood.Blood(self.x, self.y, self.angle)
                gb.effects["BloodEffect"].addBlood(self.bloodEffect)
                self.bloodSpawned = True

            self.done = True
        
        self.drawAnim.animation.updateAnimation()
        self.x += self.xVelocity
        self.y += self.yVelocity
        self.velocity *= self.vMul

    def disableEffect(self):
        if (self.bloodEffect is not None):
            self.bloodEffect.disable()

    def draw(self):
        util.blitRotate(gb.display, self.drawAnim.animation.getFrame(), [self.x, self.y], self.drawAnim.offset, -self.angle * 180 / math.pi)

class BasicHuman(entity.Entity):
    def __init__(self, x: float, y: float, name: str, characterData: dict[str, entity.AnimationComponent]):
        super(BasicHuman, self).__init__(x, y, name)
        
        self.characterData = characterData

        self.legs = characterData["IdleLegs"]
        self.body = characterData["IdleBody"]
        self.head = characterData["IdleHead"]

        self.availableWeapons = characterData["__data__"]["availableWeapons"]
        self.currentWeapon = None
        self.lastWeapon = None
        self.weaponAvailable = True
        self.weaponReady = False
        self.shouldReadyWeapon = False

        self.hp = 1

        self.hitbox: hitbox.Circle = hitbox.Circle(x, y, characterData["__data__"]["radius"])

        self.attacking = False

        self.weaponCache: dict[str, weapon.Weapon] = {}

        self.xVelocity = 0
        self.yVelocity = 0
        self.stepPlayed = False

        self.walking = False
        self.walkingMultiplier = 1

        self.sounds["WoodStep"] = [pygame.mixer.Sound(gb.baseDir + "/modules/core/assets/floors/WoodFloor/WoodFloorStep.wav"),
                                   pygame.mixer.Sound(gb.baseDir + "/modules/core/assets/floors/WoodFloor/WoodFloorStep2.wav")]

        self.pickupTime = 0

        self.holdBody: Body = None
        self.bodyHeld = False
        

        self.temp = False
        self.path: list[map.Node] = []

        for i in self.availableWeapons:
            self.weaponCache[i] = weapon.weapons[characterData["__data__"]["weapon"][i]["id"]](self)

        self.weapon = self.weaponCache["None"]

    def damage(self, x, angle, kill=True):
        reverse = self.angle

        anglediff = ((-(angle * 180 / math.pi) - reverse + 180 + 360) % 360 - 180)

        if (self.hp - x <= 0):
            gb.effects["ShakeEffect"].shake(4, .05)
            animToUse = None

            if (anglediff <= 90 and anglediff >= -90):
                animToUse = self.characterData["DeadBack"]
            else:
                animToUse = self.characterData["DeadFoward"]

            Body(self.x, self.y, animToUse, self.characterData["DeadSit"], self.characterData["DeadPicked"], angle, angle, kill)
            gb.entities.pop(self.id)
            return

    def sharedUpdate(self):
        if (abs(self.yVelocity) + abs(self.xVelocity) > 0.1):
            if (self.legs.data["componentKey"] != "WalkCycle"):
                self.legs = self.characterData["WalkCycle"]
                self.legs.animation.currentFrame = 0
                self.legs.animation.frameProgress = 0
                self.legs.animation.frameStep = .4

            self.legs.animation.frameStep = .4 * math.sqrt(self.yVelocity ** 2 + self.xVelocity ** 2) / 5
            reverse = self.angle + 180
            movementAngle = (math.atan2(self.yVelocity, self.xVelocity) * 180 / math.pi) * -1

            anglediff = (movementAngle - reverse + 180 + 360) % 360 - 180

            if (anglediff <= 90 and anglediff >= -90):
                self.legs.animation.reverse = True
            else:
                self.legs.animation.reverse = False

            if (self.legs.animation.currentFrame in self.characterData["__data__"]["stepFrames"]):
                if (not self.stepPlayed):
                    self.stepPlayed = True

                    if ((self.x // 32, self.y // 32) in gb.floors):
                        gb.floors[(self.x // 32, self.y // 32)].playSound(self.x // 32, self.y // 32, self)
                            
            else:
                self.stepPlayed = False

        else:
            self.legs = self.characterData["IdleLegs"]

        self.legs.animation.updateAnimation()
        self.head.animation.updateAnimation()
        self.body.animation.updateAnimation()

        self.hitbox.x = self.x
        self.hitbox.y = self.y

        dist = math.sqrt(self.xVelocity ** 2 + self.yVelocity ** 2)
        dist = 1 if dist == 0 else dist

        velocityLine = object.Line(self.x, self.y, self.x + self.xVelocity / dist * self.hitbox.radius, self.y + self.yVelocity / dist * self.hitbox.radius)

        pygame.draw.line(gb.display, [255, 255, 255], velocityLine.point, velocityLine.point_)

        neighbors = map.getNeighbors(self.x // 32, self.y // 32, eight=8)

        self.xVelocity, self.yVelocity, _ = map.doCollision(self.x, self.y, self.xVelocity, self.yVelocity, self.hitbox.radius)   

        self.x += self.xVelocity
        self.y += self.yVelocity


    def canSee(self, x: float, y: float):
        ray = object.Line(self.x, self.x, x, y)
        for i in gb.tileMap:
            obj = gb.tileMap[i]

            if (obj is None):
                continue

            for j in obj.visionLines:
                if (j.intersects(ray)):
                    return False
                
        return True

    def pickupBody(self, en: Body):
        ...

    def update(self):
        if (not self.temp):
            self.temp = True
            # self.path = map.findPath(self.x // 32, self.y // 32, 500 // 32, 200 // 32)

        if (len(self.path) != 0):
            dist =  abs(self.x - (self.path[0].x * 32 + 16)) + abs(self.y - (self.path[0].y * 32 + 16))
            
            if (dist < 10):
                self.path.pop(0)

            else:
                ang = math.atan2((self.path[0].y * 32 + 16) - self.y, (self.path[0].x * 32 + 16) - self.x)
                self.angle = ((ang * 180 / math.pi)) * -1
                self.xVelocity = math.cos(ang) * 3
                self.yVelocity = math.sin(ang) * 3

        else:
            self.xVelocity = 0
            self.yVelocity = 0

        self.sharedUpdate()

    def updateWeaponAnimation(self):
        if (self.attacking or not self.weapon.allowUnready):
            return

        currentWeaponData: dict[str, str] = self.characterData["__data__"]["weapon"][str(self.currentWeapon)]
        lastWeaponData: dict[str, str] = self.characterData["__data__"]["weapon"][str(self.lastWeapon)]

        if (not self.weaponAvailable):
            if (self.currentWeapon != self.lastWeapon):
                    weaponPulloutAnim = self.characterData[lastWeaponData["pullOutAnim"]]
                    weaponPulloutAnim.animation.reverse = True
                    
                    if (weaponPulloutAnim.animation.currentFrame == 0):
                        self.lastWeapon = self.currentWeapon


                    self.body = weaponPulloutAnim

            else:
                weaponPulloutAnim = self.characterData[lastWeaponData["pullOutAnim"]]
                weaponPulloutAnim.animation.reverse = False

                if (weaponPulloutAnim.animation.currentFrame == len(weaponPulloutAnim.animation.frames()) - 1):
                    self.weaponAvailable = True
                    weaponPulloutAnim.animation.reverse = False

                    self.characterData[currentWeaponData["readyAnim"]].animation.currentFrame = 0 # Reset it :)
                    self.weapon = self.weaponCache[self.currentWeapon]

                self.body = weaponPulloutAnim

        else:
            if (self.shouldReadyWeapon):
                weaponReadyAnim = self.characterData[currentWeaponData["readyAnim"]]

                if (weaponReadyAnim.animation.currentFrame == len(weaponReadyAnim.animation.frames()) - 1):
                    self.weaponReady = True
                
                weaponReadyAnim.animation.reverse = False
                self.body = weaponReadyAnim
            else:
                self.weaponReady = False
                weaponReadyAnim = self.characterData[currentWeaponData["readyAnim"]]
                
                if (weaponReadyAnim.animation.currentFrame != 0):
                    weaponReadyAnim.animation.reverse = True
                    self.body = weaponReadyAnim

    def draw(self, hitbox=False):
        angle = (math.atan2(self.yVelocity, self.xVelocity) * 180 / math.pi) * -1
        if (self.legs.animation.reverse):
            angle += 180

        # map.drawPath(self.path, [0, 255, 0])
        util.blitRotate(gb.display, self.legs.animation.getFrame(), [self.x, self.y], self.legs.offset, angle)
        util.blitRotate(gb.display, self.body.animation.getFrame(), [self.x, self.y], self.body.offset, self.angle)

        if (self.bodyHeld):
            util.blitRotate(gb.display, self.holdBody.carry.animation.getFrame(), [self.x, self.y], self.holdBody.carry.offset, self.angle)

        util.blitRotate(gb.display, self.head.animation.getFrame(), [self.x, self.y], self.head.offset, self.angle)
        if (hitbox):
            if (self.attacking):
                self.weapon.drawHitbox()
            self.hitbox.draw([255, 0, 0])

class HumanPlayer(BasicHuman):
    def __init__(self, x: float, y: float, characterData: dict[str, entity.AnimationComponent]):
        super(HumanPlayer, self).__init__(x, y, "Player", characterData)

        self.legs = characterData["IdleLegs"]
        self.body = characterData["IdleBody"]
        self.head = characterData["IdleHead"]


    def update(self):
        assinationTarget = None
        bodyTarget = None

        for i in gb.entities:
            en = gb.entities[i]

            if (en.id == self.id):
                continue

            dist = math.sqrt((self.x - en.x) ** 2 + (self.y - en.y) ** 2)
            angle = math.atan2(en.y - self.y, en.x - self.x) * 180 / math.pi
            anglediff = (angle - en.angle + 180 + 360) % 360 - 180

            if (dist < 35 and anglediff <= 90 and anglediff >= -90):
                assinationTarget = en
                break

        for i in gb.bodyentities:
            en = gb.bodyentities[i]

            dist = math.sqrt((self.x - en.x) ** 2 + (self.y - en.y) ** 2)

            if (dist < 20):
                bodyTarget = en
                break


        xdir = 0
        ydir = 0

        self.xVelocity = 0
        self.yVelocity = 0

        if (gb.keyInputs[pygame.K_LSHIFT]):
            self.walking = True
            self.walkingMultiplier = .25
        else:
            self.walking = False
            self.walkingMultiplier = 1


        if (gb.keyInputs[pygame.K_d]):
            xdir += 1

        if (gb.keyInputs[pygame.K_a]):
            xdir -= 1

        if (gb.keyInputs[pygame.K_w]):
            ydir -= 1

        if (gb.keyInputs[pygame.K_s]):
            ydir += 1


        angle = math.atan2(ydir, xdir)
        
        if (xdir != 0):
            self.xVelocity = math.cos(angle) * 3 * self.walkingMultiplier

        if (ydir != 0):
            self.yVelocity = math.sin(angle) * 3 * self.walkingMultiplier

        for i in gb.events:
            if (i.type == pygame.KEYDOWN and str(i.unicode).isnumeric() and int(i.unicode) - 1 < len(self.availableWeapons) and not self.attacking):
                if (self.weaponAvailable):
                    self.lastWeapon = self.currentWeapon
                    self.weaponAvailable = False

                self.currentWeapon = self.availableWeapons[int(i.unicode) - 1]

        if (not self.bodyHeld):
        
            if (gb.mouseInput[2] or not self.weapon.allowUnready):
                self.shouldReadyWeapon = True
            else:
                self.shouldReadyWeapon = False

            if (self.weaponAvailable and self.weaponReady):
                self.weapon.updatePlayer()

            elif (assinationTarget != None and gb.keyInputs[pygame.K_e]):
                # self.weapon.id
                print("HAHAH")

            elif (bodyTarget != None and gb.keyInputs[pygame.K_e]):
                self.pickupTime += 1

                self.body = self.characterData["PickupBody"]
                self.head = self.characterData["PickupHead"]

                self.xVelocity = 0
                self.yVelocity = 0

                if (self.pickupTime >= 60):
                    self.holdBody = gb.bodyentities.pop(bodyTarget.id)
                    self.holdBody.disableEffect()
                    self.bodyHeld = True
                    
                    self.body.animation.currentFrame = 0
                    self.head.animation.currentFrame = 0
                    
                    self.body = self.characterData["IdleBody"]
                    self.head = self.characterData["IdleHead"]

                    self.pickupTime = 0

            else:
                if (self.pickupTime != 0):
                    self.body.animation.currentFrame = 0
                    self.head.animation.currentFrame = 0
                    self.pickupTime = 0

                self.body = self.characterData["IdleBody"]
                self.head = self.characterData["IdleHead"]
        else:
            self.walkingMultiplier *= .2
            if (gb.mouseInput[0]): # holy shit
                # TODO CLEAN THIS SHIT UP
                gb.bodyentities[self.holdBody.id] = self.holdBody
                self.holdBody.vMul = .9
                self.holdBody.x = self.x
                self.holdBody.y = self.y
                self.holdBody.angle = -self.angle * math.pi / 180
                self.holdBody.vAngle = -self.angle * math.pi / 180
                self.holdBody.velocity = 10
                self.holdBody.done = False
                self.holdBody.bloodSpawned = False
                self.holdBody.collided = False
                self.holdBody.drawAnim = self.holdBody.animation
                self.holdBody = None
                self.bodyHeld = False

                self.body.animation.currentFrame = 0
                self.head.animation.currentFrame = 0

                self.body = self.characterData["IdleBody"]
                self.head = self.characterData["IdleHead"]


            elif(gb.mouseInput[1]):
                gb.bodyentities[self.holdBody.id] = self.holdBody
                self.holdBody.vMul = .8
                self.holdBody.angle = -self.angle * math.pi / 180
                self.holdBody.done = False
                self.holdBody.drawAnim = self.holdBody.animation
                self.holdBody = None
                self.bodyHeld = False

            




        self.angle = ((util.angleToPoint(gb.mousePos, (self.x, self.y)) * 180 / math.pi) + 90) * -1

        
        self.updateWeaponAnimation()
        self.sharedUpdate()

    



entity.loadCharacterData(gb.baseDir + "/modules/core/assets/bodies")
