import pygame
import numpy as np
from PIL.GifImagePlugin import GifImageFile
import math
import OpenGL.GL as GL
import OpenGL.GLU as GLU

from . import globals as gb


                

def cvtopg(image: np.ndarray):
    return pygame.image.frombuffer(image.tobytes(), image.shape[::-1], "RGBA")

def piltopg(image: GifImageFile):
    return pygame.image.frombuffer(image.tobytes(), image.size, image.mode).convert_alpha()

def surfaceToTexture( pygame_surface: pygame.Surface, textureID: list[int]):
    rgb_surface = pygame.image.tostring( pygame_surface, 'RGB')
    GL.glBindTexture(GL.GL_TEXTURE_2D, textureID[0])
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP)
    surface_rect = pygame_surface.get_rect()
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB, surface_rect.width, surface_rect.height, 0, GL.GL_RGB, GL.GL_UNSIGNED_BYTE, rgb_surface)
    GL.glGenerateMipmap(GL.GL_TEXTURE_2D)
    GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

def bindTex(textureID: list[int]):
    GL.glBindTexture(GL.GL_TEXTURE_2D, textureID[0])
    GL.glBegin(GL.GL_QUADS)
    GL.glTexCoord2f(0, 0); GL.glVertex2f(-1, 1)
    GL.glTexCoord2f(0, 1); GL.glVertex2f(-1, -1)
    GL.glTexCoord2f(1, 1); GL.glVertex2f(1, -1)
    GL.glTexCoord2f(1, 0); GL.glVertex2f(1, 1)
    GL.glEnd()

def blitRotate(surf: pygame.Surface, surf_: pygame.Surface, origin: tuple[float, float], pivot: tuple[float, float], angle: float): # https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
    image_rect = surf_.get_rect(topleft = (origin[0] - pivot[0], origin[1]-pivot[1]))
    offset_center_to_pivot: pygame.math.Vector2 = pygame.math.Vector2(origin) - image_rect.center
    
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_image_center = (origin[0] - rotated_offset.x, origin[1] - rotated_offset.y)
    
    rotated_image = pygame.transform.rotate(surf_, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
    rotated_image_rect.x -= gb.camera[0]
    rotated_image_rect.y -= gb.camera[1]

    surf.blit(rotated_image, rotated_image_rect)

def blitCamera(surf: pygame.Surface, surf_: pygame.Surface, pos: tuple[float, float] | list[float]): 
    surf.blit(surf_, (pos[0] - gb.camera[0], pos[1] - gb.camera[1]))

def angleToPoint(pos: tuple[float | int, float | int], pos_: tuple[float | int, float | int]) -> float:
    return math.atan2(pos_[1] - pos[1], pos_[0] - pos[0]) + math.pi / 2 

def colorize(surf: pygame.Surface, color: tuple[int, int, int]): # https://stackoverflow.com/questions/56209634/is-it-possible-to-change-sprite-colours-in-pygame
    im = pygame.Surface(surf.get_size())
    im.fill(color)

    im_ = surf.copy()
    im_.blit(im, (0, 0), special_flags=pygame.BLEND_MULT)

    return im_