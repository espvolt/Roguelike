from . import basicHuman
from typing import Callable



class Weapon:
    def __init__(self, owner: "basicHuman.BasicHuman"):
        self.owner = owner
        self.allowUnready = True

    def updatePlayer(self):
        pass

    def updateAi(self):
        pass

    def mainAttack(self):
        pass

    def reload(self):
        pass
    
    def drawHitbox(self):
        pass

weapons: dict[str, Callable] = {}
