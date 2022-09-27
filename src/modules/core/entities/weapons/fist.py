import math
from .. import weapon
from .... import globals as gb
from .. import basicHuman
from .... import hitbox

class Fist(weapon.Weapon):
    id = "core:Fist"
    def __init__(self, owner: basicHuman.BasicHuman):
        super(Fist, self).__init__(owner)
        
        self.currentAttack = False
        
        a1 = owner.characterData["__data__"]["weapon"]["None"]["attack1"]
        a2 = owner.characterData["__data__"]["weapon"]["None"]["attack2"]

        self.attack1 = owner.characterData[a1]
        self.attack2 = owner.characterData[a2]

        self.attackOffset = owner.characterData["__data__"]["weapon"]["None"]["attack1position"]

        self.hitbox = hitbox.Rectangle(0, 0, 5, 5, 2.5, 2.5, 0)

    def updatePlayer(self):
        if (self.hitbox.active):
            for en in list(gb.entities.values()):
                if (self.hitbox.hits(en.hitbox)):
                    print(self.owner.angle)
                    en.damage(1, self.owner.angle * math.pi / 180, kill=False)
                    ...

        if (self.owner.attacking):
            if (self.owner.body.animation.currentFrame == len(self.owner.body.animation.frames()) - 2):
                currentOffset = self.owner.body.data["offset"]
                currentOffset = (self.attackOffset[0] - currentOffset[0], self.attackOffset[1] - currentOffset[1])
                self.hitbox.x = currentOffset[0] + self.owner.x
                self.hitbox.y = currentOffset[1] + self.owner.y
                self.hitbox.x, self.hitbox.y = hitbox.Rectangle.rotatePoint((self.owner.x, self.owner.y), self.hitbox.x, self.hitbox.y, self.owner.angle * -math.pi / 180)
                self.hitbox.active = True

            if (self.owner.body.animation.currentFrame == len(self.owner.body.animation.frames()) - 1):
                self.currentAttack = not self.currentAttack
                self.owner.attacking = False
                self.hitbox.active = False

            return

        if (gb.mouseInput[0] and not self.owner.attacking):
            if (self.currentAttack):
                self.attack1.animation.currentFrame = 0
                self.owner.body = self.attack1

                self.owner.attacking = True

            else:
                self.attack2.animation.currentFrame = 0
                self.owner.body = self.attack2
                self.owner.attacking = True

    def drawHitbox(self):
        self.hitbox.draw([255, 255, 0])

weapon.weapons["core:None"] = Fist

