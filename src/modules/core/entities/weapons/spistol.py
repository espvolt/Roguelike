from asyncio import TimerHandle
import random
from .. import weapon
from .. import basicHuman
from .... import globals as gb
import math
from ...projectiles import bullet
from .... import hitbox
from .... import util
import pygame
from .... import sound
from ...effects import bullet_shell
from ...effects import shake
from ...effects import smoke

class SilencedPistol(weapon.Weapon):
    id = "core:spistol"
    def __init__(self, owner: basicHuman.BasicHuman):
        super(SilencedPistol, self).__init__(owner)
        self.soundShoot: pygame.mixer.Sound = pygame.mixer.Sound(gb.baseDir + "/modules/core/assets/weapons/SPistolShoot.wav")
        self.reloadSound: pygame.mixer.Sound = pygame.mixer.Sound(gb.baseDir + "/modules/core/assets/weapons/SPistolReload.wav")
        self.slideSound: pygame.mixer.Sound = pygame.mixer.Sound(gb.baseDir + "/modules/core/assets/weapons/SPistolSlide.wav")
        self.shellSound: pygame.mixer.Sound = pygame.mixer.Sound(gb.baseDir + "/modules/core/assets/weapons/SPistolShell.wav")
        self.unloadSound: pygame.mixer.Sound = pygame.mixer.Sound(gb.baseDir + "/modules/core/assets/weapons/SPistolUnload.wav")

        characterData = owner.characterData

        self.shootPoint = characterData["__data__"]["weapon"]["spistol"]["gunOffset"]
        self.origin = characterData[characterData["__data__"]["weapon"]["spistol"]["readyAnim"]].data["offset"]

        reloadAnimation = characterData["__data__"]["weapon"]["spistol"]["reloadAnim"]
        slideAnimation = characterData["__data__"]["weapon"]["spistol"]["slideAnim"]
        readyAnim = characterData["__data__"]["weapon"]["spistol"]["readyAnim"]

        self.reloadAnimation = characterData[reloadAnimation]
        self.slideAnim = characterData[slideAnimation]
        self.readyAnim = characterData[readyAnim]

        self.shootPoint[0] -= self.origin[0]
        self.shootPoint[1] -= self.origin[1]

        self.chamberPoint = characterData["__data__"]["weapon"]["spistol"]["chamberOffset"]

        self.chamberPoint[0] -= self.origin[0]
        self.chamberPoint[1] -= self.origin[1]

        self.insertFrame = characterData["__data__"]["weapon"]["spistol"]["insertFrame"]

        self.maxAmmo = 16
        self.ammo = self.maxAmmo
        self.reloading = False
        self.requiresChamber = False
        self.reloadSoundPlayed = False
        self.attackTime = 0
        self.dropMag = False
        self.timeHeld = 0
        
        self.pauseTimer = 0
        self.pauseThreshold = characterData["__data__"]["weapon"]["spistol"]["pauseTime"]
        self.midReloadFrame = characterData["__data__"]["weapon"]["spistol"]["midReloadFrame"]

        self.temp = 0
        self.timeSinceAttack = 0
        self.lastTimeSinceAttack = 0
        self.smokeTimer = 0
        


    def mainAttack(self):
        if (self.ammo != 0 and not self.reloading and self.attackTime <= 0):

            chamberPos = hitbox.Rectangle.rotatePoint((self.owner.x, self.owner.y), self.owner.x + self.chamberPoint[0], self.owner.y + self.chamberPoint[1], self.owner.angle * -math.pi / 180)
            pos = hitbox.Rectangle.rotatePoint((self.owner.x, self.owner.y), self.owner.x + self.shootPoint[0], self.owner.y + self.shootPoint[1], self.owner.angle * -math.pi / 180)
            
            sound.playSoundPos((gb.playerEntity.x, gb.playerEntity.y), (self.owner.x, self.owner.y), 1, self.soundShoot)
            gb.effects["ShellEffect"].appendShell(bullet_shell.Shell(chamberPos[0], chamberPos[1],
                                                  self.owner.angle, 15, 5, [255, 255, 0],
                                                  random.randint(5, 7), self.owner.angle - 90 + random.randint(-45, 45), random.randint(-50, 50)))
            gb.effects["ShakeEffect"].shake(2, .1)
            
            shootAngle = math.atan2(gb.mousePos[1] - pos[1], gb.mousePos[0] - pos[0])

            bullet.Bullet(pos[0], pos[1], shootAngle, 30, [255, 255, 0]).addTo(gb.projectiles)

            self.ammo -= 1
            self.attackTime = 5


            for _ in range(10):
                gb.effects["SmokeEffect"].addSmoke(smoke.Smoke(pos[0], pos[1], 10, .05, (self.owner.angle + 90) * math.pi / 180, 1 * math.pi / 180, 128, 2, (-(self.owner.angle + random.randint(-15, 15))) * math.pi / 180, .5, [100, 100, 100]))



            
        
        return

    def reload(self):
        if (self.ammo == self.maxAmmo):
            return
        if (self.reloading):
            return

        if (self.ammo == 0):
            self.requiresChamber = True

        self.reloading = True
        self.allowUnready = False
        
        sound.playSoundPos((gb.playerEntity.x, gb.playerEntity.y), (self.owner.x, self.owner.y), 1, self.unloadSound)

        if (not self.dropMag):
            self.reloadAnimation.animation.currentFrame = 0
        else:
            self.reloadAnimation.animation.currentFrame = len(self.reloadAnimation.animation.frames()) - 1
            self.reloadAnimation.animation.reverse = True

        self.owner.body = self.reloadAnimation

    def updatePlayer(self):
        
        if (self.reloading):
            if (self.owner.body.animation.currentFrame == self.insertFrame and not self.reloadSoundPlayed and not self.dropMag):
                self.reloadSoundPlayed = True
                sound.playSoundPos((gb.playerEntity.x, gb.playerEntity.y), (self.owner.x, self.owner.y), 1, self.reloadSound)

            if (self.dropMag):
                if (self.owner.body.animation.currentFrame == self.midReloadFrame):
                    self.owner.body.animation.paused = True

                    if (self.pauseTimer > 40):
                        self.pauseTimer = 0
                        self.owner.body.animation.paused = False
                        self.dropMag = False
                        self.owner.body.animation.reverse = False
                    else:
                        self.pauseTimer += 1

            elif (self.owner.body.animation.currentFrame == len(self.owner.body.animation.frames()) - 1):
                if (self.pauseTimer > self.pauseThreshold):
                    if (self.requiresChamber):
                        self.requiresChamber = False
                        self.slideAnim.animation.currentFrame = 0
                        self.owner.body = self.slideAnim
                        sound.playSoundPos((gb.playerEntity.x, gb.playerEntity.y), (self.owner.x, self.owner.y), 1, self.slideSound)

                    else:
                        self.reloading = False
                        self.allowUnready = True
                        self.owner.body = self.readyAnim
                        self.ammo = self.maxAmmo
                        self.reloadSoundPlayed = False
                        self.dropMag = False
                        self.pauseTimer = 0
                else:
                    self.pauseTimer += 1
                
            return

        

        


        if (gb.mouseInput[0] and not gb.jMouseInput[0]):
            self.mainAttack()
            
            return

        if (gb.keyInputs[pygame.K_r]):
            self.timeHeld += 1

            if (self.timeHeld > 20):
                self.dropMag = True
                self.reload()

        else:
            self.timeHeld = 0

        if (not gb.keyInputs[pygame.K_r] and gb.jKeyInputs[pygame.K_r]):
            self.reload()
            return

        self.attackTime = max(0, self.attackTime - 1)

    def updateAi(self):
        if (self.reloading):
            if (self.owner.body.animation.currentFrame == len(self.owner.body.animation.frames()) - 1):
                if (self.requiresChamber):
                    self.requiresChamber = False
                    self.slideAnim.animation.currentFrame = 0
                    self.owner.body = self.slideAnim

                else:
                    self.reloading = False
                    self.allowUnready = True
                    self.owner.body = self.readyAnim
                    self.ammo = self.maxAmmo
            
            return

        self.attackTime = max(0, self.attackTime - 1)


weapon.weapons["core:spistol"] = SilencedPistol