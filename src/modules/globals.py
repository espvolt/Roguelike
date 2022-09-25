import pygame
import sys
from . import scene
from . import entity
from . import object
from . import projectile
from . import effect
from . import floor

display: pygame.Surface = None
baseDir: str = sys.path[0]
currentScene: scene.Scene = None
entities: dict[int, entity.Entity] = {}
bodyentities: dict[int, entity.Entity] = {}
projectiles: dict[int, projectile.Projectile] = {}
effects: dict[str, effect.Effect] = {}
tileMap: dict[tuple[int, int], object.Object] = {}
camera: list[int, int] = [0, 0]
cameraEffect: list[int, int] = [0, 0]
mousePos: tuple[float, float]
mouseInput: tuple[bool, bool, bool] = [0, 0, 0]
jMouseInput: tuple[bool, bool, bool]
keyInputs: list[bool]
jKeyInputs: list[bool]
displayResolution: tuple[int, int] = (1280, 720)
screenResolution: tuple[int, int] = (1280, 720)
CharacterData: dict[str, dict[str, entity.AnimationComponent]] = {}
floors: dict[tuple[int, int], floor.Floor] = {}
events: list[pygame.event.Event] = []
backgroundColor = [50, 50, 50]
frameRate = 60
playerEntity: entity.Entity = None
