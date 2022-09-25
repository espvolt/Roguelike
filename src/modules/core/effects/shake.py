from ... import effect
from ... import globals as gb

import random

import numpy as np

class ShakeEffect(effect.Effect):
    def __init__(self):
        super(ShakeEffect, self).__init__("ShakeEffect")

        self.shakeModifiers = []
        self.cameraShake = [0, 0]
        
    def shake(self, mul: float, red: float):
        self.shakeModifiers.append([mul, red])

    def update(self):
        total = sum([i[0] for i in self.shakeModifiers])

        gb.camera[0] -= self.cameraShake[0]
        gb.camera[1] -= self.cameraShake[1]

        self.cameraShake[0] = random.randint(int(-total), int(total))
        self.cameraShake[1] = random.randint(int(-total), int(total))

        gb.camera[0] += self.cameraShake[0]
        gb.camera[1] += self.cameraShake[1]

        i = 0
        length = len(self.shakeModifiers)
        
        while(i != length):
            obj = self.shakeModifiers[i]

            obj[0] = max(0, abs(obj[0] - obj[1]))

            if (obj[0] < 0.01):
                self.shakeModifiers.pop(i)
                i -= 1
                length -= 1

            i += 1


ShakeEffect()





