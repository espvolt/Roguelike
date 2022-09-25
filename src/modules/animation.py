import pygame
from PIL import Image, ImageSequence

from . import util


frameCache: dict[str, list[pygame.Surface]] = {}
class Animation:
    @staticmethod
    def fromGif(src: str, cacheName: str) -> "Animation":

        f = Image.open(src)

        for frame in ImageSequence.Iterator(f):
            Animation.addFrame(cacheName, util.piltopg(frame.convert("RGBA")))
        
        f.close()

        res = Animation(0, True, cacheName)

        return res

    @staticmethod
    def image(src: str, cacheName: str):
        Animation.addFrame(cacheName, pygame.image.load(src))

        res = Animation(0, True, cacheName)

        return res

    @staticmethod
    def addFrame(name: str, surf: pygame.Surface):
        if (name not in frameCache):
            frameCache[name] = []

        frameCache[name].append(surf)

    def frames(self): # Gay
        return frameCache[self.cache]

    def __init__(self, frameStep: float, loops: bool, animationCache: str):
        self.currentFrame: int = 0
        self.frameLimit: float = 1
        self.frameProgress: float = 0
        self.frameStep: float = frameStep
        self.loops: bool = loops
        self.reverse: bool = False
        self.cache = animationCache
        self.paused = False
        
    def getFrame(self) -> pygame.Surface:
        return self.frames()[self.currentFrame]

    def updateAnimation(self):
        if (self.paused):
            return
        self.frameProgress += self.frameStep
        

        if (self.frameProgress >= self.frameLimit):
            newFrameProgress = self.frameProgress % self.frameStep
            
            if (self.currentFrame == len(self.frames()) - 1 and not self.reverse and self.loops):
                self.frameProgress = newFrameProgress
                self.currentFrame = 0

            if (self.currentFrame == 0 and self.reverse and self.loops):
                self.frameProgress = newFrameProgress
                self.currentFrame = len(self.frames()) - 1
                
            if (self.reverse):
                self.currentFrame = max(0, self.currentFrame - int(self.frameProgress / self.frameLimit))
            else:
                self.currentFrame = min(len(self.frames()) - 1, self.currentFrame + int(self.frameProgress / self.frameLimit))

            self.frameProgress = newFrameProgress
            
    