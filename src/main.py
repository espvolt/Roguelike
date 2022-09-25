from copy import copy
import importlib
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame
import modules.util as util
import modules.globals as gb

import OpenGL.GL as GL
import OpenGL.GLU as GLU

pygame.init()
pygame.mixer.init(channels=5)

fpsClock = pygame.time.Clock()

gb.display = pygame.Surface(gb.displayResolution)
screen = pygame.display.set_mode(gb.screenResolution)



for i in os.listdir(gb.baseDir + "/modules"):
    folder = gb.baseDir + "/modules/" + i

    if (os.path.isdir(folder)):
        for j in os.listdir(gb.baseDir + "/modules/" + i):

            file = gb.baseDir + "/modules/" + i + "/" + j

            if (not os.path.isfile(file) or not file.endswith(".py")):
                continue

            importName = "modules." + i + "." + j[:-3]

            mod = importlib.import_module(importName)
            mod.setup()
            
gb.jKeyInputs = pygame.key.get_pressed()

while True:
    gb.display.fill(gb.backgroundColor)
    screen.fill((0, 0, 0))

    pygame.event.pump()
    gb.events = pygame.event.get()
    for event in gb.events:
        if (event.type == pygame.QUIT):
            pygame.quit()
    
    gb.keyInputs = pygame.key.get_pressed()

    scale: tuple[float, float] = (gb.displayResolution[0] / gb.screenResolution[0], gb.displayResolution[1] / gb.screenResolution[1])

    mousePos = pygame.mouse.get_pos()
    gb.mousePos = (mousePos[0] * scale[0], mousePos[1] * scale[1])
    gb.jMouseInput = gb.mouseInput
    gb.mouseInput = pygame.mouse.get_pressed()
    
    gb.currentScene.update()
    gb.currentScene.draw()

    screen.blit(pygame.transform.scale(gb.display, gb.screenResolution), (0, 0))

    pygame.display.flip()
    fpsClock.tick(gb.frameRate)

    gb.jKeyInputs = copy(gb.keyInputs)
